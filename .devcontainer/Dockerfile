# 🔧 Imagen base actualizada (soluciona problema con libxkbcommon-x11)
FROM python:3.12-slim-bookworm

# 🔒 Buenas prácticas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# 🧑 Crear un usuario no root para desarrollo
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# 📦 Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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
    gettext \
    curl \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon0 \
    x11-utils \
    xdg-utils \
    ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 🧑 Crear el usuario no root
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# 🗂️ Copiar código fuente
COPY . /app
WORKDIR /app

# 🔒 Asignar permisos
RUN chown -R $USERNAME:$USERNAME /app

# 🔧 Usar usuario no root
USER $USERNAME

# 🐍 Actualizar pip y herramientas de build (recomendado por problemas con pkg_resources y Python 3.12)
RUN pip install --no-cache-dir --upgrade pip setuptools setuptools_scm wheel

# 🔁 Instalar proyecto en modo editable con extras para desarrollo
RUN pip install --no-cache-dir -e ".[dev,postgres]"

# 🌐 Exponer puertos
EXPOSE 5000
EXPOSE 8000

# 🔧 Comando por defecto
CMD [ "bash" ]