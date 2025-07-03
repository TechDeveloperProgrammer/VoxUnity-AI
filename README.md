# VoxUnity AI+

[![CI](https://github.com/TechDeveloperProgrammer/VoxUnity-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/TechDeveloperProgrammer/VoxUnity-AI/actions)
[![PyPI version](https://img.shields.io/pypi/v/voxunity-ai.svg)](https://pypi.org/project/voxunity-ai/)
[![Docker](https://img.shields.io/docker/v/yourdockerhub/voxunity-ai/latest)](https://hub.docker.com/r/yourdockerhub/voxunity-ai)

![VoxUnity AI+ Logo](assets/logo.png) <!-- Placeholder para un logo -->

**VoxUnity AI+** es una plataforma de código abierto de vanguardia, diseñada para empoderar a creadores de contenido, activistas, educadores y a la comunidad LGBTQIA+ con herramientas avanzadas de Inteligencia Artificial para la voz, el streaming, la seguridad, la educación inclusiva y el bienestar emocional. Nuestro objetivo es fomentar un entorno digital más inclusivo, seguro y expresivo para todos.

## Características Principales

-   **Modulación de Voz por IA (`mod-voice`):** Transforma tu voz en tiempo real con IA avanzada, aplicando presets personalizados y efectos de modulación. Integración con OBS Studio y AudioRelay para una experiencia de streaming fluida.
-   **Streaming Inclusivo (`mod-streaming`):** Mejora tus transmisiones con overlays dinámicos, alertas inclusivas personalizables y herramientas de moderación de chat impulsadas por IA para crear un espacio seguro y acogedor.
-   **Aliado y Educación (`mod-ally`):** Accede a microcursos interactivos sobre lenguaje inclusivo, diversidad y temas LGBTQIA+. Evalúa tu comprensión y recibe retroalimentación en tiempo real sobre el uso de lenguaje inclusivo.
-   **Bienestar Emocional (`mod-therapy`):** Un diario personal cifrado con análisis emocional basado en IA para ayudarte a reflexionar sobre tus sentimientos. Tus datos están protegidos con cifrado local robusto.
-   **VTuber Ready (`mod-vtuber`):** Sincronización labial (lipsync) precisa para tus avatares Live2D y VRM utilizando tu micrófono, dando vida a tus personajes virtuales.
-   **Activismo y Seguridad (`mod-activism`):** Herramientas avanzadas de OCR anti-doxing para proteger tu información personal en documentos e imágenes. Navegación anónima y comunicación segura a través de integraciones con Tor y Matrix.
-   **Educador Asistido por IA (`mod-educator`):** Genera narraciones de IA para tus materiales educativos, subtitulado automático de contenido y acceso a una biblioteca de recursos docentes curados.
-   **Movilidad y Accesibilidad (`mod-mobile`):** Interfaz de usuario de texto (TUI) optimizada para Termux en dispositivos móviles, permitiendo el uso del micrófono de tu teléfono como entrada de audio remota.
-   **Herramientas de Desarrollo (`mod-devtools`):** Una CLI avanzada para desarrolladores, con hooks de pre-commit, ejecución de tests automatizados, linters y análisis de seguridad para mantener la calidad del código.
-   **Accesibilidad Universal (`mod-accessibility`):** Navegación completa por teclado, integración con lectores de texto y temas visuales personalizables para garantizar que la aplicación sea usable por todos.

## Instalación

### Requisitos Previos

*   Python 3.9 o superior
*   `pip` (gestor de paquetes de Python)
*   `git` (para clonar el repositorio)
*   **Para Linux/macOS:** `build-essential`, `libsm6`, `libxext6`, `libxrender-dev`, `ffmpeg` (para procesamiento de audio/video).
    *   Ejemplo (Ubuntu/Debian):
        ```bash
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv build-essential libsm6 libxext6 libxrender-dev ffmpeg
        ```
*   **Para Windows:** Asegúrate de tener las herramientas de compilación de C++ (parte de Visual Studio Build Tools) si encuentras errores con ciertas librerías.
*   **Para OCR (mod-activism):** `tesseract-ocr` y `libtesseract-dev` (Linux/macOS) o el instalador de Tesseract (Windows).
*   **Para Audio (mod-voice/vtuber):** `portaudio19-dev` (Linux/macOS) o PortAudio (Windows).

### Pasos de Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/your-username/voxunity-ai.git
    cd voxunity-ai
    ```

2.  **Ejecutar el Script de Instalación:**

    *   **Linux / macOS:**
        ```bash
        ./scripts/install.sh
        ```

    *   **Termux (Android):**
        ```bash
        ./scripts/termux-install.sh
        ```

    *   **Windows (CMD/PowerShell):**
        ```cmd
        scripts\win-install.bat
        ```

    Este script creará un entorno virtual, instalará todas las dependencias necesarias y configurará la base de datos inicial. También creará un archivo `.env` a partir de `.env.example` si no existe.

3.  **Configuración Inicial (`.env`):**
    Abre el archivo `.env` en la raíz del proyecto. Es **CRÍTICO** que configures las variables `SECRET_KEY` y `ENCRYPTION_KEY` con valores únicos y seguros para tu entorno de producción. Puedes generar una `ENCRYPTION_KEY` usando Python:
    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```
    Y una `SECRET_KEY` (ej. para Flask):
    ```bash
    python -c "import os; print(os.urandom(24).hex())"
    ```

### Usando Docker (Opcional)

Para un entorno de desarrollo consistente y aislado, puedes usar Docker:

1.  **Construir la imagen Docker:**
    ```bash
    docker build -t voxunity-ai .
    ```

2.  **Ejecutar el contenedor (ej. para la API):**
    ```bash
    docker run -p 5000:5000 -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs voxunity-ai voxunity api
    ```
    Esto mapeará los directorios `data` y `logs` del contenedor a tu máquina local para persistencia.

## Uso

Una vez instalado y configurado, puedes iniciar los diferentes componentes de VoxUnity AI+:

1.  **Activar el Entorno Virtual (si no usas Docker):**
    *   **Linux / macOS / Termux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows (CMD/PowerShell):**
        ```cmd
        call venv\Scripts\activate.bat
        ```

2.  **Iniciar Componentes:**

    *   **CLI (Command Line Interface):**
        ```bash
        voxunity cli --help
        # Ejemplo: voxunity cli voice start --preset robot
        ```

    *   **GUI (Graphical User Interface):**
        ```bash
        voxunity gui
        ```

    *   **API (REST/WebSocket):**
        ```bash
        voxunity api
        ```
        La documentación interactiva de la API estará disponible en `http://127.0.0.1:5000/apidocs/` (o el puerto que configures).

### Autenticación de la API

La API requiere autenticación JWT para la mayoría de los endpoints. Primero, regístrate/inicia sesión a través del endpoint `/login` para obtener un token. Luego, incluye este token en el encabezado `Authorization` como `Bearer <your_token>`.

## Desarrollo y Contribución

¡Tu contribución es bienvenida! Consulta las siguientes guías para empezar:

*   [CONTRIBUTING.md](CONTRIBUTING.md): Guía detallada para desarrolladores.
*   [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Normas de la comunidad.
*   [SECURITY.md](SECURITY.md): Cómo reportar vulnerabilidades.
*   [Dev Container](docs/devcontainer.md): Configuración para entornos de desarrollo estandarizados (VS Code Dev Containers, GitHub Codespaces).

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para preguntas generales o soporte, por favor abre un [Issue](https://github.com/your-username/voxunity-ai/issues).

