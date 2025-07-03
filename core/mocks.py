import logging
from core.utils import get_logger

logger = get_logger(__name__)

class OBSClientMock:
    """Mock para simular la conexión y comandos de OBS Studio."""
    def __init__(self, host: str, port: int, password: str = ""):
        self.host = host
        self.port = port
        self.password = password
        self.is_connected = False
        logger.info(f"[OBSClientMock] Initialized for {host}:{port}")

    def connect(self):
        logger.info(f"[OBSClientMock] Attempting to connect to OBS at {self.host}:{self.port}...")
        # Simular un retraso o fallo
        self.is_connected = True
        logger.info("[OBSClientMock] Connected successfully.")

    def disconnect(self):
        logger.info("[OBSClientMock] Disconnecting from OBS...")
        self.is_connected = False
        logger.info("[OBSClientMock] Disconnected.")

    def set_source_filter_settings(self, source_name: str, filter_name: str, settings: dict):
        if self.is_connected:
            logger.info(f"[OBSClientMock] Setting filter '{filter_name}' for source '{source_name}' with settings: {settings}")
        else:
            logger.warning("[OBSClientMock] Not connected to OBS. Command ignored.")

    def get_version(self) -> dict:
        if self.is_connected:
            return {"obs_version": "29.1.3", "obs_websocket_version": "5.0.0"}
        return {}

class AudioRelayClientMock:
    """Mock para simular la conexión y envío de audio a AudioRelay."""
    def __init__(self, ip: str):
        self.ip = ip
        self.is_connected = False
        logger.info(f"[AudioRelayClientMock] Initialized for IP: {ip}")

    def connect(self):
        logger.info(f"[AudioRelayClientMock] Attempting to connect to AudioRelay at {self.ip}...")
        self.is_connected = True
        logger.info("[AudioRelayClientMock] Connected successfully.")

    def disconnect(self):
        logger.info("[AudioRelayClientMock] Disconnecting from AudioRelay...")
        self.is_connected = False
        logger.info("[AudioRelayClientMock] Disconnected.")

    def send_audio(self, audio_data: bytes):
        if self.is_connected:
            logger.info(f"[AudioRelayClientMock] Sending {len(audio_data)} bytes of audio data.")
        else:
            logger.warning("[AudioRelayClientMock] Not connected to AudioRelay. Audio data not sent.")

class TesseractOCRMock:
    """Mock para simular el reconocimiento OCR con Tesseract."""
    def __init__(self):
        logger.info("[TesseractOCRMock] Initialized.")

    def image_to_string(self, image_path: str, lang: str = 'eng') -> str:
        logger.info(f"[TesseractOCRMock] Performing OCR on {image_path} with language {lang}...")
        # Simular un resultado de OCR
        return f"Simulated OCR text from {os.path.basename(image_path)} in {lang}."

class WhisperModelMock:
    """Mock para simular el modelo Whisper de OpenAI para STT."""
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        logger.info(f"[WhisperModelMock] Initialized with model size: {model_size}")

    def transcribe(self, audio_path: str) -> dict:
        logger.info(f"[WhisperModelMock] Transcribing audio from {audio_path}...")
        # Simular transcripción
        return {"text": f"Simulated transcription of {os.path.basename(audio_path)}.", "language": "en"}

class BarkModelMock:
    """Mock para simular el modelo Bark para TTS."""
    def __init__(self):
        logger.info("[BarkModelMock] Initialized.")

    def generate_audio(self, text: str, voice_preset: str = "en_speaker_0") -> bytes:
        logger.info(f"[BarkModelMock] Generating audio for text (len={len(text)}) with voice preset {voice_preset}...")
        # Simular generación de audio (retorna bytes vacíos o un placeholder)
        return b"\x00\x01\x02\x03" # Pequeño placeholder de bytes

class Live2DRendererMock:
    """Mock para simular un motor de renderizado Live2D/VRM."""
    def __init__(self):
        self.model_loaded = False
        self.is_animating = False
        logger.info("[Live2DRendererMock] Initialized.")

    def load_model(self, model_path: str):
        logger.info(f"[Live2DRendererMock] Loading model: {model_path}")
        self.model_loaded = True

    def start_lipsync(self):
        if self.model_loaded:
            logger.info("[Live2DRendererMock] Starting lipsync animation.")
            self.is_animating = True
        else:
            logger.warning("[Live2DRendererMock] Cannot start lipsync: no model loaded.")

    def stop_lipsync(self):
        logger.info("[Live2DRendererMock] Stopping lipsync animation.")
        self.is_animating = False

    def update_animation(self, phoneme_data: dict):
        if self.is_animating:
            logger.info(f"[Live2DRendererMock] Updating animation with phoneme data: {phoneme_data}")

class MatrixClientMock:
    """Mock para simular un cliente Matrix."""
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.is_logged_in = False
        logger.info(f"[MatrixClientMock] Initialized for server: {server_url}")

    def login(self, username: str, password: str):
        logger.info(f"[MatrixClientMock] Attempting to log in as {username}...")
        self.is_logged_in = True
        logger.info("[MatrixClientMock] Logged in successfully.")

    def logout(self):
        logger.info("[MatrixClientMock] Logging out.")
        self.is_logged_in = False

    def send_message(self, room_id: str, message: str):
        if self.is_logged_in:
            logger.info(f"[MatrixClientMock] Sending message to room {room_id}: {message}")
        else:
            logger.warning("[MatrixClientMock] Not logged in to Matrix. Message not sent.")

class TorProxyMock:
    """Mock para simular la activación/desactivación de un proxy Tor."""
    def __init__(self, proxy_address: str):
        self.proxy_address = proxy_address
        self.is_active = False
        logger.info(f"[TorProxyMock] Initialized for proxy: {proxy_address}")

    def start(self):
        logger.info(f"[TorProxyMock] Starting Tor proxy at {self.proxy_address}...")
        self.is_active = True
        logger.info("[TorProxyMock] Tor proxy active.")

    def stop(self):
        logger.info("[TorProxyMock] Stopping Tor proxy...")
        self.is_active = False
        logger.info("[TorProxyMock] Tor proxy inactive.")

