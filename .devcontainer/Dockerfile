FROM python:3.12-slim-bullseye

# Evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Desactivar el almacenamiento en búfer de la salida estándar de Python
ENV PYTHONUNBUFFERED 1

# Crear un usuario no root para desarrollo
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
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
    # Instalar Node.js y npm para dependencias JS
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el código de la aplicación
COPY . /app
WORKDIR /app

# Cambiar el propietario del directorio de trabajo al usuario no root
RUN chown -R $USERNAME:$USERNAME /app

# Cambiar al usuario no root
USER $USERNAME

# Exponer puertos
EXPOSE 5000
EXPOSE 8000

# Comando por defecto (se ejecutará en el contenedor)
CMD ["bash"]