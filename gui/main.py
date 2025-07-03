import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget, QTabWidget, QScrollArea
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import MODULES_ENABLED, DEFAULT_LANG, SUPPORTED_LANGS, APP_NAME
from core.localization import get_translator
from core.utils import get_logger
from core.module_manager import module_manager
from gui.login_screen import LoginScreen

logger = get_logger(__name__)

class VoxUnityGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1200, 800)

        self._ = get_translator(DEFAULT_LANG)
        self.current_user_role = "guest" # Rol por defecto antes del login

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_screen = LoginScreen()
        self.login_screen.login_successful.connect(self.show_main_app)
        self.stacked_widget.addWidget(self.login_screen)

        self.main_app_widget = QWidget()
        self.main_app_layout = QVBoxLayout(self.main_app_widget)
        self.stacked_widget.addWidget(self.main_app_widget)

        self.init_main_app_ui() # Inicializar la UI principal, pero no mostrarla aún
        self.update_ui_language() # Aplicar idioma inicial

    def init_main_app_ui(self):
        # Controles superiores (selector de rol y idioma)
        top_controls_layout = QHBoxLayout()
        self.main_app_layout.addLayout(top_controls_layout)

        # Selector de rol (ahora solo muestra el rol actual)
        self.role_label = QLabel(self._("Current Role:") + f" {self.current_user_role.capitalize()}")
        top_controls_layout.addWidget(self.role_label)

        # Selector de idioma
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel(self._("Select language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(SUPPORTED_LANGS)
        self.lang_combo.setCurrentText(DEFAULT_LANG)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        top_controls_layout.addLayout(lang_layout)

        # Pestañas de módulos
        self.module_tabs = QTabWidget()
        self.main_app_layout.addWidget(self.module_tabs)

        self.modules_ui = {}

        # Crear UI para cada módulo (inicialmente ocultas)
        self.create_module_uis()

    def show_main_app(self, role: str):
        self.current_user_role = role
        self.role_label.setText(self._("Current Role:") + f" {self.current_user_role.capitalize()}")
        self.update_module_visibility()
        self.stacked_widget.setCurrentWidget(self.main_app_widget)
        logger.info(f"User logged in with role: {role}")

    def change_language(self):
        selected_lang = self.lang_combo.currentText()
        self._ = get_translator(selected_lang)
        self.update_ui_language()
        logger.info(f"Language changed to: {selected_lang}")

    def update_ui_language(self):
        self.setWindowTitle(self._("VoxUnity AI+"))
        self.login_screen._ = self._ # Actualizar traductor de la pantalla de login
        self.login_screen.init_ui() # Re-renderizar login screen con nuevo idioma

        self.role_label.setText(self._("Current Role:") + f" {self.current_user_role.capitalize()}")
        self.lang_label.setText(self._("Select language:"))
        
        # Actualizar textos de los tabs y botones
        for i in range(self.module_tabs.count()):
            tab_name_key = self.module_tabs.tabText(i).replace(" ", "_").lower() # Convertir a key de traducción
            self.module_tabs.setTabText(i, self._(tab_name_key))

        # Actualizar botones dentro de los módulos (ejemplo para Voice)
        if "mod-voice" in self.modules_ui:
            voice_widget = self.modules_ui["mod-voice"]
            voice_widget.findChild(QLabel).setText(self._("voice_module_controls"))
            voice_widget.findChild(QPushButton, "start_button").setText(self._("start"))
            voice_widget.findChild(QPushButton, "stop_button").setText(self._("stop"))

        # Repetir para otros módulos si tienen elementos de texto específicos

    def create_module_uis(self):
        # Mapeo de roles a módulos permitidos
        self.role_module_map = {
            "user": ["mod-voice", "mod-streaming", "mod-therapy", "mod-vtuber", "mod-accessibility"],
            "admin": list(MODULES_ENABLED.keys()), # Admin ve todos los módulos habilitados
            "educator": ["mod-educator", "mod-ally", "mod-voice", "mod-accessibility"],
            "activist": ["mod-activism", "mod-voice", "mod-mobile", "mod-accessibility"],
        }

        # Voice Module
        if MODULES_ENABLED.get("mod-voice"):
            self.modules_ui["mod-voice"] = self.create_voice_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-voice"], self._("voice_module"))

        # Streaming Module
        if MODULES_ENABLED.get("mod-streaming"):
            self.modules_ui["mod-streaming"] = self.create_streaming_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-streaming"], self._("streaming_module"))

        # Ally Module
        if MODULES_ENABLED.get("mod-ally"):
            self.modules_ui["mod-ally"] = self.create_ally_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-ally"], self._("ally_module"))

        # Therapy Module
        if MODULES_ENABLED.get("mod-therapy"):
            self.modules_ui["mod-therapy"] = self.create_therapy_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-therapy"], self._("therapy_module"))

        # VTuber Module
        if MODULES_ENABLED.get("mod-vtuber"):
            self.modules_ui["mod-vtuber"] = self.create_vtuber_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-vtuber"], self._("vtuber_module"))

        # Activism Module
        if MODULES_ENABLED.get("mod-activism"):
            self.modules_ui["mod-activism"] = self.create_activism_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-activism"], self._("activism_module"))

        # Educator Module
        if MODULES_ENABLED.get("mod-educator"):
            self.modules_ui["mod-educator"] = self.create_educator_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-educator"], self._("educator_module"))

        # Mobile Module
        if MODULES_ENABLED.get("mod-mobile"):
            self.modules_ui["mod-mobile"] = self.create_mobile_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-mobile"], self._("mobile_module"))

        # Devtools Module
        if MODULES_ENABLED.get("mod-devtools"):
            self.modules_ui["mod-devtools"] = self.create_devtools_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-devtools"], self._("devtools_module"))

        # Accessibility Module
        if MODULES_ENABLED.get("mod-accessibility"):
            self.modules_ui["mod-accessibility"] = self.create_accessibility_module_ui()
            self.module_tabs.addTab(self.modules_ui["mod-accessibility"], self._("accessibility_module"))

    def create_voice_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("voice_module_controls")))
        start_button = QPushButton(self._("start"))
        start_button.setObjectName("start_button")
        start_button.clicked.connect(lambda: module_manager.get_module("mod-voice").start(preset="Default"))
        stop_button = QPushButton(self._("stop"))
        stop_button.setObjectName("stop_button")
        stop_button.clicked.connect(lambda: module_manager.get_module("mod-voice").stop())
        layout.addWidget(start_button)
        layout.addWidget(stop_button)
        return widget

    def create_streaming_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("streaming_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_ally_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("ally_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_therapy_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("therapy_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_vtuber_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("vtuber_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_activism_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("activism_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_educator_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("educator_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_mobile_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("mobile_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_devtools_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("devtools_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def create_accessibility_module_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self._("accessibility_module_controls")))
        layout.addWidget(QPushButton(self._("start")))
        layout.addWidget(QPushButton(self._("stop")))
        return widget

    def update_module_visibility(self):
        allowed_modules = self.role_module_map.get(self.current_user_role, [])
        for module_name, ui_widget in self.modules_ui.items():
            # Encontrar el índice de la pestaña para el módulo actual
            tab_index = -1
            for i in range(self.module_tabs.count()):
                if self.module_tabs.widget(i) == ui_widget:
                    tab_index = i
                    break
            
            if tab_index != -1:
                if module_name in allowed_modules and MODULES_ENABLED.get(module_name, False):
                    self.module_tabs.setTabVisible(tab_index, True)
                else:
                    self.module_tabs.setTabVisible(tab_index, False)

def main():
    app = QApplication(sys.argv)
    window = VoxUnityGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()