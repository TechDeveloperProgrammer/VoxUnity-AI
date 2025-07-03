#!/bin/bash

# Script de instalación para VoxUnity AI+ (Linux/macOS)

echo "Iniciando instalación de VoxUnity AI+"

# --- 1. Instalar Python 3.12 y dependencias del sistema ---
# Detectar sistema operativo
OS_TYPE="$(uname -s)"

if [[ "$OS_TYPE" == "Linux" ]]; then
    # Para Debian/Ubuntu
    if command -v apt &> /dev/null; then
        echo "Detectado Debian/Ubuntu. Instalando dependencias del sistema..."
        sudo apt update
        sudo apt install -y python3.12 python3.12-venv python3-pip build-essential libsm6 libxext6 libxrender-dev ffmpeg tesseract-ocr libtesseract-dev portaudio19-dev gettext
    # Para Arch/Manjaro
    elif command -v pacman &> /dev/null; then
        echo "Detectado Arch/Manjaro. Instalando dependencias del sistema..."
        sudo pacman -Sy --noconfirm python python-pip python-venv base-devel libsm libxext libxrender ffmpeg tesseract tesseract-data-eng portaudio gettext
    # Para Fedora/CentOS
    elif command -v dnf &> /dev/null; then
        echo "Detectado Fedora/CentOS. Instalando dependencias del sistema..."
        sudo dnf install -y python3.12 python3.12-venv python3-pip @development-tools libSM libXext libXrender ffmpeg tesseract tesseract-langpack-eng portaudio gettext
    else
        echo "Sistema Linux no soportado directamente por este script. Por favor, instala Python 3.12 y las dependencias manualmente."
        exit 1
    fi
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "Detectado macOS. Instalando dependencias del sistema (usando Homebrew si está disponible)..."
    if command -v brew &> /dev/null; then
        brew install python@3.12 ffmpeg tesseract portaudio gettext
    else
        echo "Homebrew no encontrado. Por favor, instala Homebrew (https://brew.sh/) y luego ejecuta este script de nuevo."
        exit 1
    fi
else
    echo "Sistema operativo no soportado. Por favor, instala Python 3.12 y las dependencias manualmente."
    exit 1
fi

# --- 2. Crear y activar entorno virtual ---
echo "Creando y activando entorno virtual..."
python3.12 -m venv venv
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
echo "- OBS Studio: https://obsproject.com/ (para mod-voice, mod-streaming)"
echo "- AudioRelay: https://audiorelay.net/ (para mod-voice, mod-mobile)"
echo "---------------------------------------"

echo "\nInstalación completada. Para activar el entorno virtual, ejecuta: source venv/bin/activate"
echo "Luego puedes ejecutar: voxunity cli --help, voxunity gui, o voxunity api"