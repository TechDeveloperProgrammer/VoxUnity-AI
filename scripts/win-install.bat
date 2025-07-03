@echo off

REM Script de instalacion para Windows

echo Iniciando instalacion de VoxUnity AI+

REM --- 1. Verificar y/o instalar Python ---
where python >nul 2>nul
if %errorlevel% ne 0 (
    echo Python no encontrado. Intentando descargar e instalar Python 3.12...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python-installer.exe'"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python 3.12 instalado. Reinicia la terminal y ejecuta este script de nuevo.
    goto :eof
)

REM --- 2. Crear y activar entorno virtual ---
echo Creando y activando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

REM --- 3. Instalar dependencias de Python y el proyecto en modo editable ---
echo Instalando dependencias de Python...
pip install --upgrade pip setuptools wheel
pip install -e .[dev]

REM --- 4. Configuracion inicial ---
REM Crear archivo .env si no existe
if not exist .env (
    copy .env.example .env
    echo Archivo .env creado a partir de .env.example. Por favor, revisa y ajusta las configuraciones.
)

REM Inicializar la base de datos
echo Inicializando base de datos...
python -c "from core.database import init_db; init_db()"

REM --- 5. Referencias a instalaciones externas ---
echo.
echo --- Instalaciones Externas (Manuales) ---
echo Para una funcionalidad completa, considera instalar:
echo - OBS Studio: https://obsproject.com/ (para mod-voice, mod-streaming)
echo - AudioRelay: https://audiorelay.net/ (para mod-voice, mod-mobile)
echo ---------------------------------------
echo.
echo Instalacion completada. Para activar el entorno virtual, ejecuta: venv\Scripts\activate.bat
echo Luego puedes ejecutar: voxunity cli --help, voxunity gui, o voxunity api