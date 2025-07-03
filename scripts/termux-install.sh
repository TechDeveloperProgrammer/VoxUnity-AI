#!/bin/bash

# Script de instalación para Termux (Android)

echo "Iniciando instalación de VoxUnity AI+ en Termux"

# --- 1. Instalar dependencias del sistema Termux ---
pkg update && pkg upgrade -y
pkg install python python-pip python-venv build-essential libsm libxext libxrender ffmpeg tesseract-ocr portaudio gettext nodejs -y

# --- 2. Crear y activar entorno virtual ---
echo "Creando y activando entorno virtual..."
python -m venv venv
source venv/bin/activate

# --- 3. Instalar dependencias de Python y el proyecto en modo editable ---
echo "Instalando dependencias de Python..."
pip install --upgrade pip setuptools wheel
pip install -e .[dev]

# --- 4. Configuración inicial ---
# Crear archivo .env si no existe
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Archivo .env creado a partir de .env.example. Por favor, revisa y ajusta las configuraciones."
fi

# Inicializar la base de datos
echo "Inicializando base de datos..."
python -c "from core.database import init_db; init_db()"

# --- 5. Referencias a instalaciones externas ---
echo "\n--- Instalaciones Externas (Manuales) ---"
echo "Para una funcionalidad completa, considera instalar:"
echo "- Termux:API (para acceso a micrófono móvil)"
echo "- OBS Studio (si es posible en Android, para mod-voice, mod-streaming)"
echo "- AudioRelay (para mod-voice, mod-mobile)"
echo "---------------------------------------"

echo "\nInstalación completada en Termux. Para activar el entorno virtual, ejecuta: source venv/bin/activate"
echo "Luego puedes ejecutar: voxunity cli --help, voxunity gui, o voxunity api"