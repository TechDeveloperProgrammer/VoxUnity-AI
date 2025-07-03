import logging
import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from passlib.context import CryptContext
import jwt

# Configuración de logging (ya definida en config.py y cargada en main.py)
def get_logger(name: str) -> logging.Logger:
    """Obtiene una instancia de logger configurada."""
    return logging.getLogger(name)

def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Carga datos de un archivo JSON."""
    if not os.path.exists(filepath):
        get_logger(__name__).warning(f"File not found: {filepath}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        get_logger(__name__).error(f"Error decoding JSON from {filepath}: {e}")
        return None
    except Exception as e:
        get_logger(__name__).error(f"Error loading JSON file {filepath}: {e}")
        return None

def save_json_file(filepath: str, data: Dict[str, Any]) -> bool:
    """Guarda datos en un archivo JSON."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        get_logger(__name__).error(f"Error saving JSON file {filepath}: {e}")
        return False

def get_timestamp() -> str:
    """Retorna un timestamp formateado."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Utilidades de Seguridad ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, secret_key: str, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30) # Por defecto 30 minutos
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """Decodifica un token de acceso JWT."""
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        get_logger(__name__).warning("Token expirado.")
        return None
    except jwt.InvalidTokenError:
        get_logger(__name__).warning("Token inválido.")
        return None