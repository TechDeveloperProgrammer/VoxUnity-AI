# core/main.py
import logging
from logging.config import dictConfig
from config.config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

def get_logger(name):
    return logging.getLogger(name)

# Otras funciones de utilidad compartidas pueden ir aquí
