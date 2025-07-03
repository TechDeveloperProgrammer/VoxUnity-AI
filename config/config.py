import os
import json
import logging.handlers
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Cargar variables de entorno desde .env
load_dotenv()

# --- Configuración General de la Aplicación ---
APP_NAME = "VoxUnity AI+"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Plataforma de IA para voz, streaming, seguridad y educación inclusiva."

# --- Rutas de Directorios ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
LOCALIZATION_DIR = os.path.join(BASE_DIR, "localization")
TEMP_DIR = os.path.join(BASE_DIR, "tmp") # Directorio temporal para archivos intermedios

# Asegurarse de que los directorios necesarios existan
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# --- Configuración de la API ---
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 5000))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
API_TITLE = "VoxUnity AI+ API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API REST y WebSocket para controlar los módulos de VoxUnity AI+."

# --- Configuración de Base de Datos ---
# Por defecto SQLite, pero configurable para PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(DATA_DIR, 'voxunity.db')}")
# Ejemplo para PostgreSQL: DATABASE_URL="postgresql://user:password@host:port/dbname"
SQLALCHEMY_TRACK_MODIFICATIONS = False # Deshabilita el seguimiento de modificaciones de SQLAlchemy para mejor rendimiento

# --- Configuración de Seguridad ---
# Clave secreta para Flask (sesiones, etc.) - ¡GENERAR UNA ÚNICA Y SEGURA EN PRODUCCIÓN!
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_flask_key_change_this_in_production_12345").encode('utf-8')

# Clave de cifrado para datos sensibles (ej. diario de terapia)
# Generar con `Fernet.generate_key().decode()` y guardar en .env
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if ENCRYPTION_KEY:
    ENCRYPTION_KEY = ENCRYPTION_KEY.encode('utf-8')
else:
    # Advertencia: Esto es solo para desarrollo. En producción, la clave debe ser persistente y segura.
    print("ADVERTENCIA: ENCRYPTION_KEY no definida en .env. Generando una clave temporal. ¡NO USAR EN PRODUCCIÓN!")
    ENCRYPTION_KEY = Fernet.generate_key()
    # Opcional: guardar la clave generada en .env para la próxima vez (solo para desarrollo)
    # with open(".env", "a") as f:
    #     f.write(f"\nENCRYPTION_KEY={ENCRYPTION_KEY.decode()}\n")

# --- Configuración de Internacionalización ---
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")
SUPPORTED_LANGS = ["en", "es", "pt", "fr"]

# --- Configuración de Módulos (Habilitar/Deshabilitar) ---
MODULES_ENABLED = {
    "mod-voice": os.getenv("MODULE_VOICE_ENABLED", "True").lower() == "true",
    "mod-streaming": os.getenv("MODULE_STREAMING_ENABLED", "True").lower() == "true",
    "mod-ally": os.getenv("MODULE_ALLY_ENABLED", "True").lower() == "true",
    "mod-therapy": os.getenv("MODULE_THERAPY_ENABLED", "True").lower() == "true",
    "mod-vtuber": os.getenv("MODULE_VTUBER_ENABLED", "True").lower() == "true",
    "mod-activism": os.getenv("MODULE_ACTIVISM_ENABLED", "True").lower() == "true",
    "mod-educator": os.getenv("MODULE_EDUCATOR_ENABLED", "True").lower() == "true",
    "mod-mobile": os.getenv("MODULE_MOBILE_ENABLED", "True").lower() == "true",
    "mod-devtools": os.getenv("MODULE_DEVTOOLS_ENABLED", "True").lower() == "true",
    "mod-accessibility": os.getenv("MODULE_ACCESSIBILITY_ENABLED", "True").lower() == "true",
}

# --- Configuración Específica de Módulos (Ejemplos) ---
# Mod-Voice
VOICE_PRESETS_FILE = os.path.join(DATA_DIR, "voice_presets.json")
VOICE_DEFAULT_PRESET = "standard"
VOICE_OBS_WEBSOCKET_URL = os.getenv("VOICE_OBS_WEBSOCKET_URL", "ws://localhost:4444")
VOICE_AUDIORELAY_IP = os.getenv("VOICE_AUDIORELAY_IP", "192.168.1.100")

# Mod-Streaming
STREAMING_OVERLAYS_DIR = os.path.join(ASSETS_DIR, "overlays")
STREAMING_ALERT_SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds", "alerts")
STREAMING_MODERATION_KEYWORDS_FILE = os.path.join(DATA_DIR, "moderation_keywords.json")

# Mod-Ally
ALLY_MICROCOURSE_DIR = os.path.join(DATA_DIR, "microcourses")
ALLY_INCLUSIVE_LANGUAGE_RULES_FILE = os.path.join(DATA_DIR, "inclusive_language_rules.json")

# Mod-Therapy
THERAPY_JOURNAL_ENCRYPTED_FILE = os.path.join(DATA_DIR, "therapy_journal.enc")
THERAPY_SENTIMENT_MODEL_PATH = os.path.join(DATA_DIR, "sentiment_model.pkl") # Placeholder para modelo ML

# Mod-VTuber
VTUBER_MODELS_DIR = os.path.join(ASSETS_DIR, "vtuber_models")
VTUBER_DEFAULT_MODEL = "default_live2d.json"

# Mod-Activism
ACTIVISM_OCR_TEMP_DIR = os.path.join(TEMP_DIR, "ocr_temp")
ACTIVISM_TOR_PROXY = os.getenv("ACTIVISM_TOR_PROXY", "socks5://127.0.0.1:9050")
ACTIVISM_MATRIX_SERVER = os.getenv("ACTIVISM_MATRIX_SERVER", "https://matrix.org")

# Mod-Educator
EDUCATOR_NARRATION_OUTPUT_DIR = os.path.join(TEMP_DIR, "narrations")
EDUCATOR_SUBTITLE_OUTPUT_DIR = os.path.join(TEMP_DIR, "subtitles")
EDUCATOR_RESOURCES_DIR = os.path.join(DATA_DIR, "educator_resources")

# Mod-Mobile
MOBILE_TERMUX_CONFIG_FILE = os.path.join(DATA_DIR, "termux_config.json")

# Mod-Devtools
DEVTOOLS_TEST_REPORTS_DIR = os.path.join(LOG_DIR, "test_reports")

# Mod-Accessibility
ACCESSIBILITY_THEMES_DIR = os.path.join(ASSETS_DIR, "themes")
ACCESSIBILITY_DEFAULT_THEME = "light"

# --- Configuración de Logging ---
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'maxBytes': 10485760, # 10 MB
            'backupCount': 5,
            'formatter': 'detailed',
            'level': 'DEBUG',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10485760,
            'backupCount': 2,
            'formatter': 'detailed',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': { # Logger raíz
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': True
        },
        'api': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG' if API_DEBUG else 'INFO',
            'propagate': False
        },
        'cli': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'gui': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'plugins': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'core': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}