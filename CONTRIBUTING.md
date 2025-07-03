# Guía de Contribución a VoxUnity AI+

¡Gracias por considerar contribuir a VoxUnity AI+! Valoramos enormemente tu tiempo y esfuerzo. Esta guía te ayudará a empezar y a entender nuestro flujo de trabajo y estándares.

## Tabla de Contenidos

1.  [Cómo Empezar](#1-cómo-empezar)
    *   [Clonar el Repositorio](#clonar-el-repositorio)
    *   [Configurar el Entorno de Desarrollo](#configurar-el-entorno-de-desarrollo)
    *   [Dev Containers / Codespaces](#dev-containers--codespaces)
2.  [Flujo de Trabajo de Contribución](#2-flujo-de-trabajo-de-contribución)
    *   [Reportar Bugs](#reportar-bugs)
    *   [Sugerir Mejoras](#sugerir-mejoras)
    *   [Enviar Pull Requests](#enviar-pull-requests)
3.  [Estándares de Código](#3-estándares-de-código)
    *   [Estilo de Código](#estilo-de-código)
    *   [Type Hinting](#type-hinting)
    *   [Documentación del Código](#documentación-del-código)
    *   [Tests](#tests)
4.  [Internacionalización (i18n)](#4-internacionalización-i18n)
5.  [Estructura del Proyecto](#5-estructura-del-proyecto)
6.  [Consideraciones de Seguridad](#6-consideraciones-de-seguridad)
7.  [Código de Conducta](#7-código-de-conducta)

## 1. Cómo Empezar

### Clonar el Repositorio

```bash
git clone https://github.com/your-username/voxunity-ai.git
cd voxunity-ai
```

### Configurar el Entorno de Desarrollo

Recomendamos usar un entorno virtual para gestionar las dependencias.

1.  **Crear y Activar Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate.bat  # Windows CMD
    ```

2.  **Instalar Dependencias:**
    Instala el proyecto en modo editable junto con las dependencias de desarrollo:
    ```bash
    pip install -e .[dev]
    ```

3.  **Inicializar Base de Datos:**
    ```bash
    python -c "from core.database import init_db; init_db()"
    ```

4.  **Configurar `.env`:**
    Copia `.env.example` a `.env` y configura las claves secretas y otras variables de entorno. **¡Es crucial generar claves seguras para `SECRET_KEY` y `ENCRYPTION_KEY`!**
    ```bash
    cp .env.example .env
    # Edita .env con tus claves generadas
    ```

### Dev Containers / Codespaces

Para una configuración de entorno instantánea y consistente, recomendamos usar [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) con VS Code o [GitHub Codespaces](https://github.com/features/codespaces). El repositorio ya incluye una configuración en el directorio `.devcontainer/`.

## 2. Flujo de Trabajo de Contribución

### Reportar Bugs

Si encuentras un bug, por favor, abre un nuevo issue utilizando la plantilla `Bug Report`. Proporciona tanta información como sea posible para ayudarnos a reproducirlo y solucionarlo.

### Sugerir Mejoras

Para nuevas características o mejoras, abre un issue utilizando la plantilla `Feature Request`. Describe tu idea, el problema que resuelve y cómo crees que debería implementarse.

### Enviar Pull Requests

1.  **Haz un fork** del repositorio.
2.  **Clona tu fork** localmente.
3.  **Crea una nueva rama** para tus cambios. Usa un nombre descriptivo (ej. `feature/nombre-caracteristica`, `bugfix/descripcion-bug`).
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Realiza tus cambios.** Asegúrate de seguir los [Estándares de Código](#3-estándares-de-código).
5.  **Escribe tests** para tus cambios. Si es una nueva característica, añade tests unitarios y de integración. Si es un bugfix, añade un test que falle sin tu cambio y pase con él.
6.  **Ejecuta los tests y linters** localmente para asegurarte de que todo está correcto:
    ```bash
    pytest
    flake8 .
    mypy .
    bandit -r .
    ```
7.  **Haz commit de tus cambios.** Escribe un mensaje de commit claro y conciso que describa lo que has hecho.
    ```bash
    git commit -m "feat: Add new feature X" # o "fix: Fix bug Y"
    ```
8.  **Sube tus cambios** a tu fork:
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Abre un Pull Request (PR)** en el repositorio principal. Utiliza la plantilla `Pull Request` y describe tus cambios en detalle.

## 3. Estándares de Código

### Estilo de Código

Seguimos el estilo de código [PEP 8](https://www.python.org/dev/peps/pep-0008/). Usamos `flake8` para hacer cumplir esto. Asegúrate de que tu código pase el linter antes de enviar un PR.

### Type Hinting

Utilizamos [type hinting](https://docs.python.org/3/library/typing.html) para mejorar la legibilidad, la mantenibilidad y la detección de errores. Asegúrate de añadir type hints a tus funciones y variables. Usamos `mypy` para la verificación de tipos.

### Documentación del Código

Documenta tu código usando docstrings para módulos, clases y funciones. Explica el propósito, los argumentos, lo que retorna y cualquier excepción que pueda lanzar. Sigue el estilo [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

### Tests

Todos los cambios deben ir acompañados de tests. Utilizamos `pytest` para ejecutar nuestros tests. Los tests deben ser:

*   **Unitarios:** Prueban unidades de código individuales de forma aislada.
*   **De Integración:** Prueban la interacción entre diferentes componentes.
*   **Claros y Legibles:** Fáciles de entender y mantener.

Los tests se encuentran en el directorio `tests/`.

## 4. Internacionalización (i18n)

VoxUnity AI+ soporta múltiples idiomas. Si añades nuevas cadenas de texto visibles para el usuario, asegúrate de que sean traducibles:

1.  **Marca las cadenas:** Envuelve las cadenas de texto con la función `_()` (ej. `_("Hello World")`).
2.  **Extrae las cadenas:** Ejecuta `pygettext` para actualizar los archivos `.po`.
3.  **Traduce:** Añade las traducciones en los archivos `.po` correspondientes en `localization/<lang>/LC_MESSAGES/messages.po`.
4.  **Compila:** Compila los archivos `.po` a `.mo` usando `msgfmt`.

## 5. Estructura del Proyecto

Familiarízate con la estructura del proyecto descrita en el `README.md` para entender dónde encajan tus cambios.

## 6. Consideraciones de Seguridad

La seguridad es primordial. Sigue las mejores prácticas de seguridad al escribir código. Evita la exposición de secretos, valida siempre las entradas de usuario y utiliza las funciones de cifrado y hashing proporcionadas. Consulta `SECURITY.md` para más detalles.

## 7. Código de Conducta

Al contribuir a este proyecto, aceptas adherirte a nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Sé respetuoso y crea un ambiente acogedor para todos.