# ✅ Imagen base actualizada para evitar error con libxkbcommon-x11
FROM python:3.12-slim-bookworm

# Evitar archivos .pyc y salida con buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# 🔧 Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    git \
    tesseract-ocr \
    libtesseract-dev \
    portaudio19-dev \
    libpq-dev \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon-x11 \
    gettext \
    curl \
    # 🔧 Node.js y npm (útil para frontend, JS deps)
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 🔒 Actualizar pip, setuptools y wheel
RUN pip install --upgrade pip setuptools wheel

# 🔁 Copiar y preinstalar dependencias de Python (mejor cacheo en builds)
COPY requirements.txt .
COPY setup.py .

# ✅ Instalar las dependencias de Python (incluyendo extras de desarrollo)
RUN pip install --no-cache-dir -e .[dev]

# ⬇️ Copiar el resto del código
COPY . .

# ⚙️ Inicializar la base de datos (solo si el script es seguro en build-time)
RUN python -c "from core.database import init_db; init_db()"

# 🌐 Exponer el puerto de la API Flask
EXPOSE 5000

# 🚀 Comando de inicio por defecto
CMD ["python", "main.py", "api"]