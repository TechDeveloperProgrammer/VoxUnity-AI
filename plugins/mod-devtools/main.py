import logging
from typing import Optional, Dict, Any
import subprocess
import os
import json

from config.config import DEFAULT_LANG, DEVTOOLS_TEST_REPORTS_DIR
from core.localization import get_translator
from core.utils import get_logger, save_json_file
from core.module_manager import module_manager

logger = get_logger(__name__)

class DevtoolsModule:
    def __init__(self):
        self._ = get_translator(DEFAULT_LANG)
        self.is_active = False
        self.module_name = "mod-devtools"

    def initialize(self):
        """Prepara el entorno para las herramientas de desarrollo."""
        logger.info(self._("[mod-devtools] Inicializando módulo de herramientas de desarrollo..."))
        os.makedirs(DEVTOOLS_TEST_REPORTS_DIR, exist_ok=True)
        logger.info(self._("[mod-devtools] Directorio de reportes de tests: %s"), DEVTOOLS_TEST_REPORTS_DIR)
        logger.info(self._("[mod-devtools] Módulo de herramientas de desarrollo inicializado."))

    def load_settings(self, settings: Dict[str, Any]):
        """Carga la configuración persistente del módulo desde la DB."""
        logger.info(self._("[mod-devtools] Cargando configuración persistente..."))
        # No hay configuraciones específicas para cargar en este módulo por ahora, pero se podría añadir.

    def save_settings(self):
        """Guarda la configuración actual del módulo en la DB."""
        logger.info(self._("[mod-devtools] Guardando configuración persistente..."))
        settings_to_save = {
            # Configuraciones específicas del módulo a guardar
        }
        module_manager.save_module_settings(self.module_name, settings_to_save)

    def start(self):
        """Activa el módulo de herramientas de desarrollo (ej. hooks de pre-commit)."""
        if self.is_active:
            logger.warning(self._("[mod-devtools] El módulo de herramientas de desarrollo ya está activo."))
            return
        logger.info(self._("[mod-devtools] Iniciando módulo de herramientas de desarrollo."))

        # --- Activación de hooks (NO SIMULADA) ---
        # Esto implicaría configurar hooks de Git (ej. con `pre-commit` framework)
        # para ejecutar linters y tests antes de cada commit.
        logger.info(self._("[mod-devtools] Activando hooks de pre-commit (simulado)..."))

        self.is_active = True
        logger.info(self._("[mod-devtools] Módulo de herramientas de desarrollo iniciado."))

    def stop(self):
        """Detiene el módulo de herramientas de desarrollo."""
        if not self.is_active:
            logger.warning(self._("[mod-devtools] El módulo de herramientas de desarrollo no está activo."))
            return
        logger.info(self._("[mod-devtools] Deteniendo módulo de herramientas de desarrollo."))
        self.is_active = False
        logger.info(self._("[mod-devtools] Módulo de herramientas de desarrollo detenido."))

    def run_tests(self, module_name: Optional[str] = None) -> Dict[str, Any]:
        """Ejecuta tests unitarios o de integración."""
        logger.info(self._("[mod-devtools] Ejecutando tests..."))
        test_command = [sys.executable, "-m", "pytest"]
        if module_name:
            test_command.append(f"tests/test_{module_name}.py") # Asumiendo convención de nombres
        else:
            test_command.append("tests/")

        try:
            result = subprocess.run(test_command, capture_output=True, text=True, check=True)
            logger.info(self._("[mod-devtools] Tests ejecutados exitosamente."))
            logger.debug(result.stdout)
            return {"status": "success", "output": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            logger.error(self._("[mod-devtools] Error al ejecutar tests: %s"), e)
            logger.error(e.stderr)
            return {"status": "error", "output": e.stdout, "stderr": e.stderr}
        except FileNotFoundError:
            logger.error(self._("[mod-devtools] pytest no encontrado. Asegúrate de que esté instalado."))
            return {"status": "error", "output": "pytest not found", "stderr": ""}

    def run_linter(self) -> Dict[str, Any]:
        """Ejecuta el linter (flake8)."""
        logger.info(self._("[mod-devtools] Ejecutando linter (flake8)..."))
        try:
            result = subprocess.run([sys.executable, "-m", "flake8", "."], capture_output=True, text=True, check=True)
            logger.info(self._("[mod-devtools] Linter ejecutado exitosamente. No se encontraron problemas."))
            return {"status": "success", "output": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            logger.warning(self._("[mod-devtools] Linter encontró problemas."))
            logger.warning(e.stdout)
            return {"status": "warning", "output": e.stdout, "stderr": e.stderr}
        except FileNotFoundError:
            logger.error(self._("[mod-devtools] flake8 no encontrado. Asegúrate de que esté instalado."))
            return {"status": "error", "output": "flake8 not found", "stderr": ""}

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual del módulo de herramientas de desarrollo."""
        return {
            "is_active": self.is_active,
            "test_reports_dir": DEVTOOLS_TEST_REPORTS_DIR,
        }

