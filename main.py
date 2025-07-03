import argparse
import sys
import os
import logging

# Añadir el directorio raíz del proyecto al PATH para importaciones relativas
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config.config import LOGGING_CONFIG
from core.utils import get_logger
from core.module_manager import module_manager

# Configurar logging al inicio
logging.config.dictConfig(LOGGING_CONFIG)
logger = get_logger(__name__)

def run_cli():
    from cli.main import main as cli_main
    cli_main()

def run_gui():
    from gui.main import main as gui_main
    gui_main()

def run_api():
    from api.app import main as api_main
    api_main()

def main():
    parser = argparse.ArgumentParser(description="VoxUnity AI+ Unified Launcher")
    parser.add_argument("component", choices=["cli", "gui", "api"], help="Component to run (cli, gui, api)")

    args = parser.parse_args()

    # Inicializar módulos antes de lanzar el componente principal
    module_manager.initialize_modules()

    if args.component == "cli":
        logger.info("Launching VoxUnity AI+ CLI...")
        run_cli()
    elif args.component == "gui":
        logger.info("Launching VoxUnity AI+ GUI...")
        run_gui()
    elif args.component == "api":
        logger.info("Launching VoxUnity AI+ API...")
        run_api()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()