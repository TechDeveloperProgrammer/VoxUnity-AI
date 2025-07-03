import logging
from typing import Dict, Any, Optional

from config.config import MODULES_ENABLED
from core.utils import get_logger
from core.database import get_db, ModuleSetting
from sqlalchemy.orm import Session
import json

# Importar todas las clases de módulos
from plugins.mod_voice.main import VoiceModule
from plugins.mod_streaming.main import StreamingModule
from plugins.mod_ally.main import AllyModule
from plugins.mod_therapy.main import TherapyModule
from plugins.mod_vtuber.main import VTuberModule
from plugins.mod_activism.main import ActivismModule
from plugins.mod_educator.main import EducatorModule
from plugins.mod_mobile.main import MobileModule
from plugins.mod_devtools.main import DevtoolsModule
from plugins.mod_accessibility.main import AccessibilityModule

logger = get_logger(__name__)

class ModuleManager:
    _instance = None
    _modules: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModuleManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize_modules(self):
        if self._initialized:
            logger.info("Module Manager already initialized.")
            return

        logger.info("Initializing Module Manager and enabled modules...")
        module_classes = {
            "mod-voice": VoiceModule,
            "mod-streaming": StreamingModule,
            "mod-ally": AllyModule,
            "mod-therapy": TherapyModule,
            "mod-vtuber": VTuberModule,
            "mod-activism": ActivismModule,
            "mod-educator": EducatorModule,
            "mod-mobile": MobileModule,
            "mod-devtools": DevtoolsModule,
            "mod-accessibility": AccessibilityModule,
        }

        for module_name, module_class in module_classes.items():
            if MODULES_ENABLED.get(module_name, False):
                try:
                    instance = module_class()
                    self._modules[module_name] = instance
                    logger.info(f"Module '{module_name}' instance created.")
                    
                    # Cargar configuración persistente del módulo
                    db: Session
                    for db in get_db():
                        settings_record = db.query(ModuleSetting).filter_by(module_name=module_name).first()
                        if settings_record:
                            settings = json.loads(settings_record.settings_json)
                            instance.load_settings(settings) # Asume que cada módulo tiene un método load_settings
                            logger.info(f"Loaded persistent settings for module '{module_name}'.")
                        break

                    instance.initialize() # Llamar al método initialize de cada módulo
                    logger.info(f"Module '{module_name}' initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize module '{module_name}': {e}")
                    # Considerar deshabilitar el módulo si falla la inicialización crítica
                    MODULES_ENABLED[module_name] = False
            else:
                logger.info(f"Module '{module_name}' is disabled by configuration.")
        
        self._initialized = True
        logger.info("All enabled modules initialized.")

    def get_module(self, module_name: str) -> Optional[Any]:
        """Retorna una instancia de un módulo si está habilitado e inicializado."""
        if not self._initialized:
            self.initialize_modules()
        
        if MODULES_ENABLED.get(module_name, False):
            return self._modules.get(module_name)
        else:
            logger.warning(f"Attempted to access disabled or uninitialized module: {module_name}")
            return None

    def save_module_settings(self, module_name: str, settings: Dict[str, Any]):
        """Guarda la configuración de un módulo de forma persistente en la DB."""
        db: Session
        for db in get_db():
            settings_record = db.query(ModuleSetting).filter_by(module_name=module_name).first()
            if settings_record:
                settings_record.settings_json = json.dumps(settings)
                logger.info(f"Updated settings for module '{module_name}'.")
            else:
                new_settings = ModuleSetting(module_name=module_name, settings_json=json.dumps(settings))
                db.add(new_settings)
                logger.info(f"Created new settings for module '{module_name}'.")
            db.commit()
            break

    def get_all_module_statuses(self) -> Dict[str, Any]:
        """Retorna el estado de todos los módulos inicializados."""
        statuses = {}
        for module_name, instance in self._modules.items():
            try:
                statuses[module_name] = instance.get_status()
            except Exception as e:
                logger.error(f"Error getting status for module '{module_name}': {e}")
                statuses[module_name] = {"error": str(e), "is_active": False}
        return statuses

# Instancia global del ModuleManager
module_manager = ModuleManager()
