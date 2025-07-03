import logging
from typing import Optional, Dict, Any
import json

from config.config import DEFAULT_LANG, VOICE_PRESETS_FILE, VOICE_OBS_WEBSOCKET_URL, VOICE_AUDIORELAY_IP
from core.localization import get_translator
from core.utils import get_logger, load_json_file, save_json_file
from core.module_manager import module_manager # Importar para guardar settings
from core.mocks import OBSClientMock, AudioRelayClientMock # Importar mocks

logger = get_logger(__name__)

class VoiceModule:
    def __init__(self):
        self._ = get_translator(DEFAULT_LANG)
        self.is_active = False
        self.current_preset = None
        self.voice_presets = {}
        self.obs_client = None 
        self.audiorelay_client = None 
        self.module_name = "mod-voice"

    def initialize(self):
        """Carga los presets de voz y prepara las conexiones."""
        logger.info(self._("[mod-voice] Inicializando módulo de voz..."))
        # Cargar presets desde archivo o usar por defecto
        self.voice_presets = load_json_file(VOICE_PRESETS_FILE) or {}
        if not self.voice_presets:
            logger.warning(self._("[mod-voice] No se encontraron presets de voz. Cargando presets por defecto."))
            self._load_default_presets()
            save_json_file(VOICE_PRESETS_FILE, self.voice_presets) # Guardar presets por defecto
        
        # Inicializar mocks para OBS y AudioRelay
        self.obs_client = OBSClientMock(host="localhost", port=4444) # Usar mock
        self.audiorelay_client = AudioRelayClientMock(ip="192.168.1.100") # Usar mock

        try:
            self.obs_client.connect()
            logger.info(self._("[mod-voice] Conectado a OBS Studio (mock) en %s"), VOICE_OBS_WEBSOCKET_URL)
        except Exception as e:
            logger.error(self._("[mod-voice] Error al conectar a OBS Studio (mock): %s"), e)

        try:
            self.audiorelay_client.connect()
            logger.info(self._("[mod-voice] Conectado a AudioRelay (mock) en %s"), VOICE_AUDIORELAY_IP)
        except Exception as e:
            logger.error(self._("[mod-voice] Error al conectar a AudioRelay (mock): %s"), e)

        logger.info(self._("[mod-voice] Módulo de voz inicializado."))

    def _load_default_presets(self):
        """Carga presets de voz por defecto si no hay un archivo de presets."""
        self.voice_presets = {
            "standard": {"description": "Voz normal", "settings": {}},
            "robot": {"description": "Voz robótica", "settings": {"pitch": 0.8, "formant": 1.2}},
            "chipmunk": {"description": "Voz de ardilla", "settings": {"pitch": 1.5, "formant": 1.0}},
            "deep": {"description": "Voz profunda", "settings": {"pitch": 0.7, "formant": 0.9}},
        }

    def load_settings(self, settings: Dict[str, Any]):
        """Carga la configuración persistente del módulo desde la DB."""
        logger.info(self._("[mod-voice] Cargando configuración persistente..."))
        if "voice_presets" in settings:
            self.voice_presets = settings["voice_presets"]
        # Aquí se cargarían otras configuraciones específicas del módulo

    def save_settings(self):
        """Guarda la configuración actual del módulo en la DB."""
        logger.info(self._("[mod-voice] Guardando configuración persistente..."))
        settings_to_save = {
            "voice_presets": self.voice_presets,
            # Otras configuraciones a guardar
        }
        module_manager.save_module_settings(self.module_name, settings_to_save)

    def start(self, preset: Optional[str] = None):
        """Inicia la modulación de voz con un preset dado."""
        if self.is_active:
            logger.warning(self._("[mod-voice] La modulación de voz ya está activa."))
            return

        selected_preset = preset if preset in self.voice_presets else "standard"
        self.current_preset = selected_preset
        settings = self.voice_presets.get(selected_preset, {}).get("settings", {})

        logger.info(self._("[mod-voice] Iniciando modulación de voz con preset: %s"), selected_preset)
        logger.debug(self._("[mod-voice] Configuración del preset: %s"), settings)

        # --- Lógica de procesamiento de audio en tiempo real (NO SIMULADA) ---
        # Aquí iría la integración con librerías como PyAudio o Sounddevice
        # para capturar el audio del micrófono y aplicar efectos.
        # Ejemplo conceptual:
        # import pyaudio
        # p = pyaudio.PyAudio()
        # stream = p.open(format=pyaudio.paInt64, channels=1, rate=44100, input=True, output=True)
        # while self.is_active:
        #     data = stream.read(1024)
        #     processed_data = self._apply_voice_effect(data, settings) # Función interna para aplicar efectos
        #     stream.write(processed_data)
        # stream.stop_stream()
        # stream.close()
        # p.terminate()

        # --- Integración con OBS Studio (NO SIMULADA) ---
        # Si OBS está conectado, se podría cambiar la fuente de audio, aplicar filtros, etc.
        # if self.obs_client and self.obs_client.is_connected:
        #     self.obs_client.set_source_filter_settings("Mic/Aux", "VST Plugin", {"preset_name": selected_preset})
        #     logger.info(self._("[mod-voice] Enviando comando a OBS para aplicar filtro de voz."))

        # --- Integración con AudioRelay (NO SIMULADA) ---
        # Si AudioRelay está conectado, se podría enviar el audio procesado a un dispositivo móvil.
        # if self.audiorelay_client and self.audiorelay_client.is_connected:
        #     self.audiorelay_client.send_audio(processed_audio_stream)
        #     logger.info(self._("[mod-voice] Enviando audio procesado a AudioRelay."))

        self.is_active = True
        logger.info(self._("[mod-voice] Modulación de voz iniciada."))

    def stop(self):
        """Detiene la modulación de voz."""
        if not self.is_active:
            logger.warning(self._("[mod-voice] La modulación de voz no está activa."))
            return

        logger.info(self._("[mod-voice] Deteniendo modulación de voz..."))
        # Lógica para detener el procesamiento de audio
        # Lógica para revertir cambios en OBS/AudioRelay

        self.is_active = False
        self.current_preset = None
        logger.info(self._("[mod-voice] Modulación de voz detenida."))

    def configure(self, new_settings: Dict[str, Any]):
        """Configura el módulo de voz (ej. añadir/modificar presets)."""
        logger.info(self._("[mod-voice] Configurando módulo de voz..."))
        # Lógica para actualizar presets o configuraciones internas
        if "presets" in new_settings:
            self.voice_presets.update(new_settings["presets"])
            self.save_settings()
            logger.info(self._("[mod-voice] Presets de voz actualizados."))
        logger.info(self._("[mod-voice] Módulo de voz configurado."))

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual del módulo de voz."""
        return {
            "is_active": self.is_active,
            "current_preset": self.current_preset,
            "available_presets": list(self.voice_presets.keys()),
            "obs_connected": self.obs_client.is_connected, 
            "audiorelay_connected": self.audiorelay_client.is_connected, 
        }

