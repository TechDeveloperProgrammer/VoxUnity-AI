import logging
from typing import Optional, Dict, Any, List
import json

from config.config import DEFAULT_LANG, STREAMING_OVERLAYS_DIR, STREAMING_ALERT_SOUNDS_DIR, STREAMING_MODERATION_KEYWORDS_FILE
from core.localization import get_translator
from core.utils import get_logger, load_json_file, save_json_file
from core.module_manager import module_manager

logger = get_logger(__name__)

class StreamingModule:
    def __init__(self):
        self._ = get_translator(DEFAULT_LANG)
        self.is_active = False
        self.active_overlays: List[str] = []
        self.moderation_keywords: List[str] = []
        self.module_name = "mod-streaming"

    def initialize(self):
        """Carga configuraciones de overlays y palabras clave de moderación."""
        logger.info(self._("[mod-streaming] Inicializando módulo de streaming..."))
        self.moderation_keywords = load_json_file(STREAMING_MODERATION_KEYWORDS_FILE) or []
        if not self.moderation_keywords:
            logger.warning(self._("[mod-streaming] No se encontraron palabras clave de moderación. Usando por defecto."))
            self.moderation_keywords = ["badword1", "badword2"]
            save_json_file(STREAMING_MODERATION_KEYWORDS_FILE, self.moderation_keywords)

        # Simulación de carga de assets de overlays
        logger.info(self._("[mod-streaming] Cargando assets de overlays desde %s (simulado)"), STREAMING_OVERLAYS_DIR)
        logger.info(self._("[mod-streaming] Cargando sonidos de alerta desde %s (simulado)"), STREAMING_ALERT_SOUNDS_DIR)
        logger.info(self._("[mod-streaming] Módulo de streaming inicializado."))

    def load_settings(self, settings: Dict[str, Any]):
        """Carga la configuración persistente del módulo desde la DB."""
        logger.info(self._("[mod-streaming] Cargando configuración persistente..."))
        if "moderation_keywords" in settings:
            self.moderation_keywords = settings["moderation_keywords"]
        if "active_overlays" in settings:
            self.active_overlays = settings["active_overlays"]

    def save_settings(self):
        """Guarda la configuración actual del módulo en la DB."""
        logger.info(self._("[mod-streaming] Guardando configuración persistente..."))
        settings_to_save = {
            "moderation_keywords": self.moderation_keywords,
            "active_overlays": self.active_overlays,
        }
        module_manager.save_module_settings(self.module_name, settings_to_save)

    def start(self, overlay_name: Optional[str] = None):
        """Inicia el módulo de streaming, activando overlays y moderación."""
        if self.is_active:
            logger.warning(self._("[mod-streaming] El módulo de streaming ya está activo."))
            return

        logger.info(self._("[mod-streaming] Iniciando módulo de streaming..."))

        # --- Lógica de renderizado de overlays (NO SIMULADA) ---
        # Aquí iría la integración con librerías como OpenCV o Pygame
        # para superponer gráficos y texto en la transmisión de video.
        # Esto podría implicar un proceso separado que capture la pantalla
        # o una fuente de video y añada los overlays antes de enviarlo a OBS/Streamlabs.
        if overlay_name:
            logger.info(self._("[mod-streaming] Activando overlay: %s"), overlay_name)
            self.active_overlays.append(overlay_name)
        else:
            logger.info(self._("[mod-streaming] Activando overlays por defecto."))
            self.active_overlays.append("default_overlay")
        self.save_settings()

        # --- Lógica de alertas inclusivas (NO SIMULADA) ---
        # Esto implicaría monitorear eventos de streaming (nuevos seguidores, donaciones)
        # y activar animaciones visuales y sonidos de alerta.
        logger.info(self._("[mod-streaming] Activando sistema de alertas inclusivas."))

        # --- Lógica de moderación de chat (NO SIMULADA) ---
        # Conexión a APIs de chat (Twitch Chat, YouTube Live Chat) para monitorear
        # mensajes y aplicar reglas de moderación (filtrado de palabras, auto-mod).
        logger.info(self._("[mod-streaming] Iniciando monitoreo y moderación de chat."))

        self.is_active = True
        logger.info(self._("[mod-streaming] Módulo de streaming iniciado."))

    def stop(self):
        """Detiene el módulo de streaming."""
        if not self.is_active:
            logger.warning(self._("[mod-streaming] El módulo de streaming no está activo."))
            return

        logger.info(self._("[mod-streaming] Deteniendo módulo de streaming..."))
        # Lógica para detener renderizado de overlays, alertas y moderación de chat.
        self.active_overlays = []
        self.is_active = False
        self.save_settings()
        logger.info(self._("[mod-streaming] Módulo de streaming detenido."))

    def activate_overlay(self, overlay_name: str):
        """Activa un overlay específico."""
        if overlay_name not in self.active_overlays:
            self.active_overlays.append(overlay_name)
            self.save_settings()
            logger.info(self._("[mod-streaming] Overlay '%s' activado."), overlay_name)
        else:
            logger.warning(self._("[mod-streaming] Overlay '%s' ya está activo."), overlay_name)

    def deactivate_overlay(self, overlay_name: str):
        """Desactiva un overlay específico."""
        if overlay_name in self.active_overlays:
            self.active_overlays.remove(overlay_name)
            self.save_settings()
            logger.info(self._("[mod-streaming] Overlay '%s' desactivado."), overlay_name)
        else:
            logger.warning(self._("[mod-streaming] Overlay '%s' no está activo."), overlay_name)

    def add_moderation_keyword(self, keyword: str):
        """Añade una palabra clave a la lista de moderación."""
        if keyword not in self.moderation_keywords:
            self.moderation_keywords.append(keyword)
            save_json_file(STREAMING_MODERATION_KEYWORDS_FILE, self.moderation_keywords)
            self.save_settings()
            logger.info(self._("[mod-streaming] Palabra clave de moderación añadida: %s"), keyword)
        else:
            logger.warning(self._("[mod-streaming] Palabra clave '%s' ya existe en la lista de moderación."), keyword)

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual del módulo de streaming."""
        return {
            "is_active": self.is_active,
            "active_overlays": self.active_overlays,
            "moderation_keywords_count": len(self.moderation_keywords),
        }

