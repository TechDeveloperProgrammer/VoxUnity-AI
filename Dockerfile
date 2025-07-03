FROM python:3.12-slim-bullseye

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    git \
    # Dependencias para tesseract (si se usa en mod-activism)
    tesseract-ocr \
    libtesseract-dev \
    # Dependencias para pyaudio (si se usa en mod-voice/vtuber)
    portaudio19-dev \
    # Dependencias para psycopg2 (si se usa PostgreSQL)
    libpq-dev \
    # Dependencias para GUI (PyQt5)
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon-x11 \
    # Para gettext
    gettext \
    # Para Node.js y npm (si se usan dependencias JS)
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt y setup.py para instalar dependencias
COPY requirements.txt .
COPY setup.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -e .[dev]

# Copiar el resto del código de la aplicación
COPY . .

# Inicializar la base de datos al construir la imagen (para desarrollo)
RUN python -c "from core.database import init_db; init_db()"

# Exponer el puerto de la API
EXPOSE 5000

# Comando por defecto para ejecutar la API (se puede sobrescribir)
CMD ["python", "main.py", "api"]
