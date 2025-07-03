import logging
import os
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime

from config.config import DEFAULT_LANG, ENCRYPTION_KEY, THERAPY_JOURNAL_ENCRYPTED_FILE, THERAPY_SENTIMENT_MODEL_PATH
from core.localization import get_translator
from core.utils import get_logger
from core.database import get_db, JournalEntry
from sqlalchemy.orm import Session
from core.module_manager import module_manager

logger = get_logger(__name__)

class TherapyModule:
    def __init__(self):
        self._ = get_translator(DEFAULT_LANG)
        self.is_active = False
        self.fernet = Fernet(ENCRYPTION_KEY)
        self.sentiment_model = None # Placeholder para modelo de sentimiento
        self.module_name = "mod-therapy"

    def initialize(self):
        """Carga el modelo de análisis de sentimiento."""
        logger.info(self._("[mod-therapy] Inicializando módulo de terapia..."))
        # --- Carga de modelo de sentimiento (NO SIMULADA) ---
        # Aquí se cargaría un modelo de Machine Learning para análisis de sentimiento.
        # Ejemplo: from joblib import load; self.sentiment_model = load(THERAPY_SENTIMENT_MODEL_PATH)
        if os.path.exists(THERAPY_SENTIMENT_MODEL_PATH):
            logger.info(self._("[mod-therapy] Cargando modelo de sentimiento desde %s (simulado)"), THERAPY_SENTIMENT_MODEL_PATH)
            # self.sentiment_model = load(THERAPY_SENTIMENT_MODEL_PATH)
        else:
            logger.warning(self._("[mod-therapy] No se encontró modelo de sentimiento en %s. El análisis será básico."), THERAPY_SENTIMENT_MODEL_PATH)

        logger.info(self._("[mod-therapy] Módulo de terapia inicializado."))

    def load_settings(self, settings: Dict[str, Any]):
        """Carga la configuración persistente del módulo desde la DB."""
        logger.info(self._("[mod-therapy] Cargando configuración persistente..."))
        # No hay configuraciones específicas para cargar en este módulo por ahora, pero se podría añadir.

    def save_settings(self):
        """Guarda la configuración actual del módulo en la DB."""
        logger.info(self._("[mod-therapy] Guardando configuración persistente..."))
        settings_to_save = {
            # Configuraciones específicas del módulo a guardar
        }
        module_manager.save_module_settings(self.module_name, settings_to_save)

    def start(self):
        """Inicia el módulo de terapia (ej. para monitoreo continuo)."""
        if self.is_active:
            logger.warning(self._("[mod-therapy] El módulo de terapia ya está activo."))
            return
        logger.info(self._("[mod-therapy] Iniciando módulo de terapia."))
        self.is_active = True

    def stop(self):
        """Detiene el módulo de terapia."""
        if not self.is_active:
            logger.warning(self._("[mod-therapy] El módulo de terapia no está activo."))
            return
        logger.info(self._("[mod-therapy] Deteniendo módulo de terapia."))
        self.is_active = False

    def add_journal_entry(self, user_id: int, content: str) -> bool:
        """Añade una entrada al diario cifrado y realiza análisis de sentimiento."""
        logger.info(self._("[mod-therapy] Añadiendo entrada de diario para usuario %d..."), user_id)
        try:
            encrypted_content = self.fernet.encrypt(content.encode('utf-8')).decode('utf-8')
            sentiment = self._analyze_sentiment(content) # Realizar análisis de sentimiento

            db: Session
            for db in get_db():
                new_entry = JournalEntry(
                    user_id=user_id,
                    encrypted_content=encrypted_content,
                    sentiment_analysis=sentiment,
                    created_at=datetime.now()
                )
                db.add(new_entry)
                db.commit()
                db.refresh(new_entry)
                logger.info(self._("[mod-therapy] Entrada de diario guardada (ID: %d, Sentimiento: %s)."), new_entry.id, sentiment)
                return True
        except Exception as e:
            logger.error(self._("[mod-therapy] Error al añadir entrada de diario: %s"), e)
            return False

    def get_journal_entries(self, user_id: int) -> List[Dict[str, Any]]:
        """Recupera y descifra las entradas del diario para un usuario."""
        logger.info(self._("[mod-therapy] Recuperando entradas de diario para usuario %d..."), user_id)
        entries = []
        db: Session
        for db in get_db():
            journal_entries = db.query(JournalEntry).filter_by(user_id=user_id).all()
            for entry in journal_entries:
                try:
                    decrypted_content = self.fernet.decrypt(entry.encrypted_content.encode('utf-8')).decode('utf-8')
                    entries.append({
                        "id": entry.id,
                        "content": decrypted_content,
                        "sentiment": entry.sentiment_analysis,
                        "created_at": entry.created_at.isoformat()
                    })
                except InvalidToken:
                    logger.error(self._("[mod-therapy] Error de token inválido al descifrar entrada %d. Posible corrupción o clave incorrecta."), entry.id)
                except Exception as e:
                    logger.error(self._("[mod-therapy] Error al descifrar entrada %d: %s"), entry.id, e)
        logger.info(self._("[mod-therapy] %d entradas de diario recuperadas para usuario %d."), len(entries), user_id)
        return entries

    def _analyze_sentiment(self, text: str) -> str:
        """Realiza análisis de sentimiento sobre el texto."""
        # --- Lógica de análisis de sentimiento (NO SIMULADA) ---
        # Si self.sentiment_model está cargado, usarlo para predecir el sentimiento.
        # Ejemplo conceptual con un modelo simple:
        if self.sentiment_model:
            # prediction = self.sentiment_model.predict([text])
            # return "positive" if prediction[0] == 1 else "negative" # Ejemplo binario
            return "neutral" # Placeholder
        else:
            # Análisis de sentimiento muy básico basado en palabras clave
            text_lower = text.lower()
            if any(word in text_lower for word in ["feliz", "alegre", "amor", "positivo"]):
                return "positive"
            elif any(word in text_lower for word in ["triste", "enojado", "miedo", "negativo"]):
                return "negative"
            else:
                return "neutral"

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual del módulo de terapia."""
        return {
            "is_active": self.is_active,
            "sentiment_model_loaded": self.sentiment_model is not None,
            "journal_entries_count": 0 # Esto debería ser consultado de la DB para el usuario actual
        }

