import logging
from typing import Optional, Dict, Any, List
import json

from config.config import DEFAULT_LANG, ALLY_MICROCOURSE_DIR, ALLY_INCLUSIVE_LANGUAGE_RULES_FILE
from core.localization import get_translator
from core.utils import get_logger, load_json_file, save_json_file
from core.module_manager import module_manager

logger = get_logger(__name__)

class AllyModule:
    def __init__(self):
        self._ = get_translator(DEFAULT_LANG)
        self.is_active = False
        self.current_course = None
        self.inclusive_language_rules = {}
        self.module_name = "mod-ally"

    def initialize(self):
        """Carga las reglas de lenguaje inclusivo y los microcursos disponibles."""
        logger.info(self._("[mod-ally] Inicializando módulo Ally..."))
        self.inclusive_language_rules = load_json_file(ALLY_INCLUSIVE_LANGUAGE_RULES_FILE) or {}
        if not self.inclusive_language_rules:
            logger.warning(self._("[mod-ally] No se encontraron reglas de lenguaje inclusivo. Usando por defecto."))
            self._load_default_language_rules()
            save_json_file(ALLY_INCLUSIVE_LANGUAGE_RULES_FILE, self.inclusive_language_rules)

        # Simulación de carga de microcursos
        logger.info(self._("[mod-ally] Cargando microcursos desde %s (simulado)"), ALLY_MICROCOURSE_DIR)
        logger.info(self._("[mod-ally] Módulo Ally inicializado."))

    def _load_default_language_rules(self):
        """Carga reglas de lenguaje inclusivo por defecto."""
        self.inclusive_language_rules = {
            "gendered_terms": {
                "male": ["hombre", "chico", "ellos"], # Ejemplo simplificado
                "female": ["mujer", "chica", "ellas"],
                "neutral": ["persona", "individuo", "elles"],
            },
            "ableist_terms": ["ciego", "sordo", "loco"], # Ejemplo
        }

    def load_settings(self, settings: Dict[str, Any]):
        """Carga la configuración persistente del módulo desde la DB."""
        logger.info(self._("[mod-ally] Cargando configuración persistente..."))
        if "inclusive_language_rules" in settings:
            self.inclusive_language_rules = settings["inclusive_language_rules"]

    def save_settings(self):
        """Guarda la configuración actual del módulo en la DB."""
        logger.info(self._("[mod-ally] Guardando configuración persistente..."))
        settings_to_save = {
            "inclusive_language_rules": self.inclusive_language_rules,
        }
        module_manager.save_module_settings(self.module_name, settings_to_save)

    def start(self, course_name: Optional[str] = None):
        """Inicia un microcurso o el módulo de análisis de lenguaje."""
        if self.is_active:
            logger.warning(self._("[mod-ally] El módulo Ally ya está activo."))
            return

        logger.info(self._("[mod-ally] Iniciando módulo Ally..."))

        if course_name:
            logger.info(self._("[mod-ally] Cargando microcurso: %s"), course_name)
            self.current_course = course_name
            # --- Lógica de carga y presentación del microcurso (NO SIMULADA) ---
            # Esto implicaría cargar contenido de texto/multimedia, gestionar el progreso del usuario,
            # y presentar preguntas de evaluación.
        else:
            logger.info(self._("[mod-ally] Iniciando análisis de lenguaje inclusivo en tiempo real."))
            # --- Lógica de análisis de lenguaje en tiempo real (NO SIMULADA) ---
            # Integración con librerías de PNL (spaCy, NLTK) para analizar texto de entrada
            # (ej. de un chat, un documento) e identificar términos no inclusivos
            # o sugerir alternativas.

        self.is_active = True
        logger.info(self._("[mod-ally] Módulo Ally iniciado."))

    def stop(self):
        """Detiene el módulo Ally."""
        if not self.is_active:
            logger.warning(self._("[mod-ally] El módulo Ally no está activo."))
            return

        logger.info(self._("[mod-ally] Deteniendo módulo Ally..."))
        self.current_course = None
        self.is_active = False
        logger.info(self._("[mod-ally] Módulo Ally detenido."))

    def analyze_text_for_inclusivity(self, text: str) -> Dict[str, Any]:
        """Analiza un texto para identificar lenguaje no inclusivo."""
        logger.info(self._("[mod-ally] Analizando texto para inclusividad..."))
        findings = {"non_inclusive_terms": [], "suggestions": []}

        # --- Lógica de análisis de PNL (NO SIMULADA) ---
        # Iterar sobre el texto y comparar con las reglas de self.inclusive_language_rules
        # Ejemplo muy simplificado:
        for term_type, terms in self.inclusive_language_rules.items():
            if term_type == "gendered_terms":
                for gender, words in terms.items():
                    if gender != "neutral":
                        for word in words:
                            if word in text.lower():
                                findings["non_inclusive_terms"].append(word)
                                findings["suggestions"].append(f"Consider using neutral terms instead of '{word}'.")
            elif term_type == "ableist_terms":
                for word in terms:
                    if word in text.lower():
                        findings["non_inclusive_terms"].append(word)
                        findings["suggestions"].append(f"Consider rephrasing '{word}' to be more inclusive.")

        logger.info(self._("[mod-ally] Análisis de inclusividad completado. Hallazgos: %s"), findings)
        return findings

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual del módulo Ally."""
        return {
            "is_active": self.is_active,
            "current_course": self.current_course,
            "rules_loaded": bool(self.inclusive_language_rules),
        }

