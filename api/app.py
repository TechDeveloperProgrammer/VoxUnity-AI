import sys
import os
import logging
from logging.config import dictConfig
from functools import wraps

from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flasgger import Swagger, swag_from
from pydantic import ValidationError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import API_HOST, API_PORT, API_DEBUG, LOGGING_CONFIG, MODULES_ENABLED, DEFAULT_LANG, API_TITLE, API_VERSION, API_DESCRIPTION, SECRET_KEY
from core.localization import get_translator
from core.utils import get_logger, create_access_token, decode_access_token
from core.database import get_db, User
from core.module_manager import module_manager
from api.models import ApiResponse, VoiceControlRequest, JournalEntryCreate, AnonymizeFileRequest, NarrationRequest, RunTestsRequest, ApplyThemeRequest, LoginRequest, TokenResponse, StreamingControlRequest

# Configurar logging
dictConfig(LOGGING_CONFIG)
logger = get_logger(__name__)

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SWAGGER'] = {
    'title': API_TITLE,
    'uiversion': API_VERSION,
    'description': API_DESCRIPTION,
    'specs_route': '/swagger/',
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        }
    }
}
swagger = Swagger(app)

# Middleware para internacionalización
@app.before_request
def set_language():
    lang = request.headers.get('Accept-Language', DEFAULT_LANG).split(',')[0].split('-')[0]
    request.locale = get_translator(lang)

# Decorador para requerir autenticación JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        _ = request.locale
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify(ApiResponse(status="error", message=_("Token is missing!")).dict()), 401

        try:
            data = decode_access_token(token, SECRET_KEY)
            if data is None:
                return jsonify(ApiResponse(status="error", message=_("Token is invalid or expired!")).dict()), 401
            
            # Obtener usuario de la DB y adjuntarlo a `g` (global request object)
            db = next(get_db()) # Obtener una sesión de DB
            user = db.query(User).filter_by(username=data['sub']).first()
            if not user:
                return jsonify(ApiResponse(status="error", message=_("User not found!")).dict()), 401
            g.current_user = user
            g.db = db # Adjuntar la sesión de DB a g para que los recursos la usen

        except Exception as e:
            logger.error(_("Error during token validation: %s"), e)
            return jsonify(ApiResponse(status="error", message=_("Token is invalid or expired!")).dict()), 401

        return f(*args, **kwargs)
    return decorated

# Manejo global de errores de validación de Pydantic
@app.errorhandler(ValidationError)
def handle_pydantic_validation_error(error):
    _ = request.locale
    logger.error(_("Pydantic Validation Error: %s"), error.errors())
    return jsonify(ApiResponse(status="error", message=_("Validation error"), data=error.errors()).dict()), 400

# --- Endpoints de Autenticación ---
class Login(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': LoginRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Login successful',
                'schema': TokenResponse.schema()
            },
            401: {
                'description': 'Invalid credentials',
                'schema': ApiResponse.schema()
            }
        }
    })
    def post(self):
        """
        User Login
        Authenticates a user and returns an access token.
        ---
        tags:
          - Authentication
        """
        _ = request.locale
        try:
            data = LoginRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

        db = next(get_db())
        user = db.query(User).filter_by(username=data.username).first()
        db.close() # Cerrar la sesión de DB después de usarla

        if not user or not user.verify_password(data.password):
            return jsonify(ApiResponse(status="error", message=_("Invalid username or password")).dict()), 401

        token = create_access_token(data={"sub": user.username, "role": user.role}, secret_key=SECRET_KEY)
        return jsonify(TokenResponse(access_token=token, token_type="bearer").dict()), 200

api.add_resource(Login, '/login')

# --- Endpoints Generales ---
class Status(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'API status and enabled modules',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required # Requiere token para acceder al estado
    def get(self):
        """
        Get API Status
        This endpoint provides the current status of the API and lists enabled modules.
        ---
        tags:
          - General
        security:
          - BearerAuth: []
        """
        _ = request.locale
        logger.info(_("GET request to API status by user: %s"), g.current_user.username)
        return jsonify(ApiResponse(status="success", message=_("API is running"), data={"modules_enabled": MODULES_ENABLED, "current_user": g.current_user.username, "current_role": g.current_user.role, "module_statuses": module_manager.get_all_module_statuses()}).dict())

api.add_resource(Status, '/status')

# --- Endpoints de Módulos ---

# Mod-Voice
class VoiceResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Voice module status',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Voice module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def get(self):
        """
        Get Voice Module Status
        ---
        tags:
          - Voice Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-voice"):
            logger.warning(_("Attempted to access disabled Voice module"))
            return jsonify(ApiResponse(status="error", message=_('Voice module is disabled')).dict()), 403
        
        module = module_manager.get_module("mod-voice")
        if module:
            return jsonify(ApiResponse(status="success", message=_('Voice module is active'), data=module.get_status()).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Voice module not initialized')).dict()), 500

    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': VoiceControlRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Action performed successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Voice module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Control Voice Module
        Starts or stops voice modulation with an optional preset.
        ---
        tags:
          - Voice Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-voice"):
            logger.warning(_("Attempted to control disabled Voice module"))
            return jsonify(ApiResponse(status="error", message=_('Voice module is disabled')).dict()), 403

        try:
            data = VoiceControlRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

        module = module_manager.get_module("mod-voice")
        if not module:
            return jsonify(ApiResponse(status="error", message=_('Voice module not initialized')).dict()), 500

        if data.action == "start":
            module.start(preset=data.preset)
            logger.info(_("Starting voice modulation with preset: %s"), data.preset)
            return jsonify(ApiResponse(status="success", message=_('Voice modulation started'), data=data.dict()).dict()), 200
        elif data.action == "stop":
            module.stop()
            logger.info(_("Stopping voice modulation"))
            return jsonify(ApiResponse(status="success", message=_('Voice modulation stopped')).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Invalid action')).dict()), 400

api.add_resource(VoiceResource, '/modules/voice')

# Mod-Streaming
class StreamingResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Streaming module status',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Streaming module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def get(self):
        """
        Get Streaming Module Status
        ---
        tags:
          - Streaming Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-streaming"):
            logger.warning(_("Attempted to access disabled Streaming module"))
            return jsonify(ApiResponse(status="error", message=_('Streaming module is disabled')).dict()), 403
        
        module = module_manager.get_module("mod-streaming")
        if module:
            return jsonify(ApiResponse(status="success", message=_('Streaming module is active'), data=module.get_status()).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Streaming module not initialized')).dict()), 500

    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': StreamingControlRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Action performed successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Streaming module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Control Streaming Module
        Starts or stops streaming features or activates/deactivates overlays.
        ---
        tags:
          - Streaming Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-streaming"):
            logger.warning(_("Attempted to control disabled Streaming module"))
            return jsonify(ApiResponse(status="error", message=_('Streaming module is disabled')).dict()), 403

        try:
            data = StreamingControlRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

        module = module_manager.get_module("mod-streaming")
        if not module:
            return jsonify(ApiResponse(status="error", message=_('Streaming module not initialized')).dict()), 500

        if data.action == "start":
            module.start()
            logger.info(_("Starting streaming features."))
            return jsonify(ApiResponse(status="success", message=_('Streaming features started')).dict()), 200
        elif data.action == "stop":
            module.stop()
            logger.info(_("Stopping streaming features."))
            return jsonify(ApiResponse(status="success", message=_('Streaming features stopped')).dict()), 200
        elif data.action == "activate_overlay":
            module.activate_overlay(data.overlay_name)
            logger.info(_("Activating overlay: %s"), data.overlay_name)
            return jsonify(ApiResponse(status="success", message=_('Overlay activated'), data=data.dict()).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Invalid action')).dict()), 400

api.add_resource(StreamingResource, '/modules/streaming')

# Mod-Ally
class AllyResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Ally module status',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Ally module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def get(self):
        """
        Get Ally Module Status
        ---
        tags:
          - Ally Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-ally"):
            logger.warning(_("Attempted to access disabled Ally module"))
            return jsonify(ApiResponse(status="error", message=_('Ally module is disabled')).dict()), 403
        
        module = module_manager.get_module("mod-ally")
        if module:
            return jsonify(ApiResponse(status="success", message=_('Ally module is active'), data=module.get_status()).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Ally module not initialized')).dict()), 500

    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': JournalEntryCreate.schema() # Reutilizando para ejemplo, debería ser un modelo Ally específico
        }],
        'responses': {
            200: {
                'description': 'Action performed successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Ally module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Control Ally Module
        Starts or stops ally features or processes text for inclusivity.
        ---
        tags:
          - Ally Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-ally"):
            logger.warning(_("Attempted to control disabled Ally module"))
            return jsonify(ApiResponse(status="error", message=_('Ally module is disabled')).dict()), 403

        try:
            data = request.get_json() # Usar directamente para flexibilidad en este ejemplo
            action = data.get("action")
            text_to_analyze = data.get("text")
        except Exception as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=str(e)).dict()), 400

        module = module_manager.get_module("mod-ally")
        if not module:
            return jsonify(ApiResponse(status="error", message=_('Ally module not initialized')).dict()), 500

        if action == "start":
            module.start()
            logger.info(_("Starting Ally module features."))
            return jsonify(ApiResponse(status="success", message=_('Ally module started')).dict()), 200
        elif action == "stop":
            module.stop()
            logger.info(_("Stopping Ally module features."))
            return jsonify(ApiResponse(status="success", message=_('Ally module stopped')).dict()), 200
        elif action == "analyze_text" and text_to_analyze:
            analysis_result = module.analyze_text_for_inclusivity(text_to_analyze)
            logger.info(_("Analyzing text for inclusivity: %s"), text_to_analyze[:50] + "...")
            return jsonify(ApiResponse(status="success", message=_('Text analysis complete'), data={"original_text": text_to_analyze, "analysis_result": analysis_result}).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Invalid action or missing text')).dict()), 400

api.add_resource(AllyResource, '/modules/ally')

# Mod-Therapy
class TherapyResource(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': JournalEntryCreate.schema()
        }],
        'responses': {
            200: {
                'description': 'Journal entry added',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Therapy module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Add Journal Entry
        Adds an encrypted journal entry and performs sentiment analysis.
        ---
        tags:
          - Therapy Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-therapy"):
            return jsonify(ApiResponse(status="error", message=_('Therapy module is disabled')).dict()), 403
        try:
            data = JournalEntryCreate(**request.get_json())
            module = module_manager.get_module("mod-therapy")
            if not module:
                return jsonify(ApiResponse(status="error", message=_('Therapy module not initialized')).dict()), 500
            
            module.add_journal_entry(user_id=g.current_user.id, content=data.content)
            logger.info(_("Adding journal entry for user %s: %s"), g.current_user.username, data.content[:50] + "...")
            return jsonify(ApiResponse(status="success", message=_('Journal entry added')).dict()), 200
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

api.add_resource(TherapyResource, '/modules/therapy/journal')

# Mod-VTuber
class VTuberResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'VTuber module status',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'VTuber module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def get(self):
        """
        Get VTuber Module Status
        ---
        tags:
          - VTuber Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-vtuber"):
            logger.warning(_("Attempted to access disabled VTuber module"))
            return jsonify(ApiResponse(status="error", message=_('VTuber module is disabled')).dict()), 403
        
        module = module_manager.get_module("mod-vtuber")
        if module:
            return jsonify(ApiResponse(status="success", message=_('VTuber module is active'), data=module.get_status()).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('VTuber module not initialized')).dict()), 500

    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': VoiceControlRequest.schema() # Reutilizando para ejemplo, debería ser un modelo VTuber específico
        }],
        'responses': {
            200: {
                'description': 'Action performed successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'VTuber module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Control VTuber Module
        Starts or stops VTuber features or loads a model.
        ---
        tags:
          - VTuber Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-vtuber"):
            logger.warning(_("Attempted to control disabled VTuber module"))
            return jsonify(ApiResponse(status="error", message=_('VTuber module is disabled')).dict()), 403

        try:
            data = request.get_json() # Usar directamente para flexibilidad en este ejemplo
            action = data.get("action")
            model_name = data.get("model")
        except Exception as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=str(e)).dict()), 400

        module = module_manager.get_module("mod-vtuber")
        if not module:
            return jsonify(ApiResponse(status="error", message=_('VTuber module not initialized')).dict()), 500

        if action == "start":
            module.start()
            logger.info(_("Starting VTuber module features."))
            return jsonify(ApiResponse(status="success", message=_('VTuber module started')).dict()), 200
        elif action == "stop":
            module.stop()
            logger.info(_("Stopping VTuber module features."))
            return jsonify(ApiResponse(status="success", message=_('VTuber module stopped')).dict()), 200
        elif action == "load_model" and model_name:
            module.start(model_name=model_name)
            logger.info(_("Loading VTuber model: %s"), model_name)
            return jsonify(ApiResponse(status="success", message=_('VTuber model loaded'), data={"model_name": model_name}).dict()), 200
        else:
            return jsonify(ApiResponse(status="error", message=_('Invalid action or missing model name')).dict()), 400

api.add_resource(VTuberResource, '/modules/vtuber')

# Mod-Activism
class ActivismResource(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': AnonymizeFileRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'File anonymized successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Activism module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Anonymize File
        Performs OCR anti-doxing and anonymization on a given file.
        ---
        tags:
          - Activism Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-activism"):
            return jsonify(ApiResponse(status="error", message=_('Activism module is disabled')).dict()), 403
        try:
            data = AnonymizeFileRequest(**request.get_json())
            module = module_manager.get_module("mod-activism")
            if not module:
                return jsonify(ApiResponse(status="error", message=_('Activism module not initialized')).dict()), 500
            
            module.anonymize_file(data.file_path)
            logger.info(_("Anonymizing file for user %s: %s"), g.current_user.username, data.file_path)
            return jsonify(ApiResponse(status="success", message=_('File anonymized successfully')).dict()), 200
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

api.add_resource(ActivismResource, '/modules/activism/anonymize')

# Mod-Educator
class EducatorResource(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': NarrationRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Narration generated successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Educator module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Generate AI Narration
        Converts text to speech using AI.
        ---
        tags:
          - Educator Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-educator"):
            return jsonify(ApiResponse(status="error", message=_('Educator module is disabled')).dict()), 403
        try:
            data = NarrationRequest(**request.get_json())
            module = module_manager.get_module("mod-educator")
            if not module:
                return jsonify(ApiResponse(status="error", message=_('Educator module not initialized')).dict()), 500
            
            module.generate_narration(data.text, data.language)
            logger.info(_("Generating narration for user %s: %s"), g.current_user.username, data.text[:50] + "...")
            return jsonify(ApiResponse(status="success", message=_('Narration generated'), data={"audio_url": "/path/to/audio.mp3"}).dict()), 200
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

api.add_resource(EducatorResource, '/modules/educator/narrate')

# Mod-Devtools
class DevtoolsResource(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': RunTestsRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Tests executed successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Devtools module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Run Tests
        Executes unit or integration tests for specified modules.
        ---
        tags:
          - Devtools Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-devtools"):
            return jsonify(ApiResponse(status="error", message=_('Devtools module is disabled')).dict()), 403
        try:
            data = RunTestsRequest(**request.get_json())
            module = module_manager.get_module("mod-devtools")
            if not module:
                return jsonify(ApiResponse(status="error", message=_('Devtools module not initialized')).dict()), 500
            
            module.run_tests(data.module_name)
            logger.info(_("Running tests for user %s, module: %s"), g.current_user.username, data.module_name if data.module_name else "all")
            return jsonify(ApiResponse(status="success", message=_('Tests executed')).dict()), 200
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

api.add_resource(DevtoolsResource, '/modules/devtools/run_tests')

# Mod-Accessibility
class AccessibilityResource(Resource):
    @swag_from({
        'parameters': [{
            'in': 'body',
            'name': 'body',
            'schema': ApplyThemeRequest.schema()
        }],
        'responses': {
            200: {
                'description': 'Theme applied successfully',
                'schema': ApiResponse.schema()
            },
            400: {
                'description': 'Invalid request',
                'schema': ApiResponse.schema()
            },
            403: {
                'description': 'Accessibility module is disabled',
                'schema': ApiResponse.schema()
            }
        }
    })
    @token_required
    def post(self):
        """
        Apply Theme
        Applies a visual theme to the application.
        ---
        tags:
          - Accessibility Module
        security:
          - BearerAuth: []
        """
        _ = request.locale
        if not MODULES_ENABLED.get("mod-accessibility"):
            return jsonify(ApiResponse(status="error", message=_('Accessibility module is disabled')).dict()), 403
        try:
            data = ApplyThemeRequest(**request.get_json())
            module = module_manager.get_module("mod-accessibility")
            if not module:
                return jsonify(ApiResponse(status="error", message=_('Accessibility module not initialized')).dict()), 500
            
            module.apply_theme(data.theme_name)
            logger.info(_("Applying theme for user %s: %s"), g.current_user.username, data.theme_name)
            return jsonify(ApiResponse(status="success", message=_('Theme applied')).dict()), 200
        except ValidationError as e:
            return jsonify(ApiResponse(status="error", message=_("Invalid request data"), data=e.errors()).dict()), 400

api.add_resource(AccessibilityResource, '/modules/accessibility/apply_theme')

# --- WebSocket Events ---
@socketio.on('connect')
def handle_connect():
    _ = request.locale
    logger.info(_('Client connected to WebSocket'))
    emit('response', {'data': _('Connected to VoxUnity AI+ WebSocket')})

@socketio.on('disconnect')
def handle_disconnect():
    _ = request.locale
    logger.info(_('Client disconnected from WebSocket'))

@socketio.on('message')
def handle_message(message):
    _ = request.locale
    logger.info(_('Received WebSocket message: %s'), message)
    emit('response', {'data': _('Echo: ') + str(message)})

@socketio.on('voice_command')
def handle_voice_command(data):
    _ = request.locale
    action = data.get('action')
    preset = data.get('preset')
    logger.info(_('Received voice command via WebSocket: Action=%s, Preset=%s'), action, preset)
    # Aquí se integraría la lógica real del módulo de voz
    emit('voice_status', {'status': _('processing'), 'action': action, 'preset': preset})

def main():
    # Inicializar módulos antes de iniciar la API
    module_manager.initialize_modules()

    if API_DEBUG:
        app.run(debug=True, host=API_HOST, port=API_PORT)
    else:
        socketio.run(app, host=API_HOST, port=API_PORT, debug=False, allow_unsafe_werkzeug=True) # allow_unsafe_werkzeug para evitar advertencias en producción

if __name__ == '__main__':
    main()
