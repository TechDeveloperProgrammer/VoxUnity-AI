# 📌 Imagen base actualizada y estable con Python 3.12 y soporte de GUI (libxkbcommon, mesa, etc.)
FROM python:3.12-slim-bookworm

# 🔒 Buenas prácticas para evitar archivos `.pyc` y errores por salida bufferizada
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 🧑 Crear variables para usuario seguro de desarrollo
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# 📦 Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    gettext \
    ca-certificates \
    ffmpeg \
    tesseract-ocr \
    libtesseract-dev \
    portaudio19-dev \
    libpq-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    x11-utils \
    xdg-utils \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 👤 Crear usuario no root para evitar uso de root en contenedor
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# 🗂️ Establecer directorio de trabajo
WORKDIR /app

# 🔁 Copiar solo lo necesario primero (para cacheo eficiente en builds sucesivos)
COPY setup.py requirements.txt pyproject.toml ./

# 🐍 Actualizar herramientas esenciales de Python
RUN pip install --upgrade pip setuptools wheel

# ⚙️ Instalar el proyecto con extras (editable)
RUN pip install -e ".[dev,postgres]"

# 📦 Copiar el resto del código fuente
COPY . .

# 🔐 Asignar permisos de la app al usuario no root
RUN chown -R $USERNAME:$USERNAME /app

# 👤 Cambiar al usuario no root
USER $USERNAME

# 🌐 Exponer puertos (Flask, socketio, API)
EXPOSE 5000 8000

# 🏁 Comando por defecto (puedes cambiarlo a `["python", "main.py"]` si deseas ejecutarlo directo)
CMD ["bash"]