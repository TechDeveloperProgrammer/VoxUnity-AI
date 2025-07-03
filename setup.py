from setuptools import setup, find_packages

setup(
    name="voxunity-ai",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    install_requires=[
        "Flask~=2.3.0",
        "Flask-RESTful~=0.3.9",
        "Flask-SocketIO~=5.3.0",
        "python-engineio~=4.3.0",
        "python-socketio~=5.8.0",
        "PyQt5~=5.15.0", # Para la GUI
        "PyQt5-tools~=5.15.0", # Para herramientas de diseño de PyQt5
        "SpeechRecognition~=3.10.0", # Para reconocimiento de voz
        "pydub~=0.25.0", # Para manipulación de audio
        "opencv-python~=4.8.0", # Para procesamiento de imágenes (OCR, overlays)
        "Pillow~=10.0.0", # Para manipulación de imágenes
        "requests~=2.31.0",
        "beautifulsoup4~=4.12.0",
        "scikit-learn~=1.3.0", # Para análisis de texto/emocional
        "numpy~=1.25.0",
        "pandas~=2.0.0",
        "matplotlib~=3.7.0",
        "Flasgger~=0.9.7", # Para documentación OpenAPI
        "gTTS~=2.3.0", # Para texto a voz en módulo Educator
        "pycryptodome~=3.19.0", # Para cifrado en módulo Therapy
        "langdetect~=1.0.9", # Para detección de idioma
        "pygettext~=1.0", # Para internacionalización
        "polib~=1.1.0", # Para internacionalización
        "python-dotenv~=1.0.0", # Para gestión de variables de entorno
        "SQLAlchemy~=1.4.0", # ORM para base de datos
        "Click~=8.1.0", # Para la CLI
        "Pydantic~=1.10.0", # Para validación de esquemas
        "python-multipart~=0.0.6", # Para Flasgger con Pydantic
        "cryptography~=41.0.0", # Para Fernet encryption
        "passlib~=1.7.0", # Para hashing de contraseñas
        "pyjwt~=2.8.0", # Para JWT
    ],
    extras_require={
        'dev': [
            'pytest~=7.4.0',
            'flake8~=6.1.0',
            'mypy~=1.5.0',
            'bandit~=1.7.0',
            'mkdocs~=1.5.0',
            'mkdocs-material~=9.4.0',
        ],
        'postgres': [
            'psycopg2-binary~=2.9.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "voxunity=main:main", # Punto de entrada unificado
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Education",
        "Topic :: Sociology",
    ],
    python_requires=">=3.9",
)