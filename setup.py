from setuptools import setup, find_packages

setup(
    name="voxunity-ai",
    version="0.1.0",
    description="Plataforma avanzada de inteligencia artificial emocional, educativa y social.",
    author="VoxUnity Team",
    license="MIT",
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        # Framework principal
        "Flask~=2.3.0",
        "Flask-RESTful~=0.3.9",
        "Flask-SocketIO~=5.3.0",

        # Comunicación en tiempo real
        "python-engineio~=4.3.0",
        "python-socketio~=5.8.0",

        # Interfaz gráfica
        "PyQt5~=5.15.0",
        "PyQt5-tools~=5.15.0",

        # Procesamiento de audio y voz
        "SpeechRecognition~=3.10.0",
        "pydub~=0.25.0",
        "gTTS~=2.3.0",

        # Procesamiento de imágenes y video
        "opencv-python~=4.8.0",
        "Pillow~=10.0.0",

        # NLP y análisis de texto
        "scikit-learn~=1.3.0",
        "numpy~=1.25.0",
        "pandas~=2.0.0",
        "langdetect~=1.0.9",

        # Seguridad y cifrado
        "pycryptodome~=3.19.0",
        "cryptography~=41.0.0",
        "passlib~=1.7.0",
        "pyjwt~=2.8.0",

        # Backend y APIs
        "requests~=2.31.0",
        "SQLAlchemy~=1.4.0",
        "python-dotenv~=1.0.0",
        "python-multipart~=0.0.6",

        # CLI & validaciones
        "Click~=8.1.0",
        "Pydantic~=1.10.0",

        # Documentación y APIs
        "Flasgger~=0.9.7",
        "beautifulsoup4~=4.12.0",

        # Internacionalización
        "pygettext~=1.0",
        "polib~=1.1.0",

        # Visualización
        "matplotlib~=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest~=7.4.0",
            "flake8~=6.1.0",
            "mypy~=1.5.0",
            "bandit~=1.7.0",
            "mkdocs~=1.5.0",
            "mkdocs-material~=9.4.0",
            "setuptools~=69.0.0",
            "setuptools_scm~=8.0.0",
            "wheel~=0.42.0",
        ],
        "postgres": [
            "psycopg2-binary~=2.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "voxunity=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Security",
        "Topic :: Education",
        "Topic :: Sociology",
    ],
)