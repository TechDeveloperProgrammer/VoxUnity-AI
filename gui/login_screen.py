from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSignal

from core.utils import get_logger
from core.localization import get_translator
from core.database import get_db, User
from sqlalchemy.orm import Session

logger = get_logger(__name__)

class LoginScreen(QWidget):
    login_successful = pyqtSignal(str) # Emite el rol del usuario

    def __init__(self):
        super().__init__()
        self._ = get_translator('en') # Idioma por defecto para la pantalla de login
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Título
        title_label = QLabel(self._("Welcome to VoxUnity AI+"))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        layout.addStretch(1)

        # Username
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel(self._("Username:")))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self._("Enter your username"))
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel(self._("Password:")))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self._("Enter your password"))
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Role Selection (for new users or demo)
        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel(self._("Select Role (for demo/new user):")))
        self.role_combo = QComboBox()
        self.role_combo.addItems([self._("User"), self._("Admin"), self._("Educator"), self._("Activist")])
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # Login Button
        login_button = QPushButton(self._("Login / Register (Demo)"))
        login_button.clicked.connect(self.attempt_login)
        layout.addWidget(login_button)

        layout.addStretch(1)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        selected_role = self.role_combo.currentText().lower() # Convertir a minúsculas para consistencia

        if not username or not password:
            QMessageBox.warning(self, self._("Login Error"), self._("Please enter both username and password."))
            return

        # Simulación de login/registro con DB
        db: Session
        for db in get_db(): # Usar el generador de sesión de DB
            user = db.query(User).filter_by(username=username).first()

            if user:
                # Usuario existente, verificar contraseña
                if user.verify_password(password):
                    logger.info(f"User {username} logged in with role {user.role}")
                    self.login_successful.emit(user.role)
                else:
                    QMessageBox.warning(self, self._("Login Error"), self._("Invalid password."))
                    logger.warning(f"Failed login attempt for user {username}: Invalid password.")
            else:
                # Nuevo usuario, registrar
                new_user = User(username=username, password=password, role=selected_role)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                logger.info(f"New user {username} registered with role {selected_role}")
                QMessageBox.information(self, self._("Registration Successful"), self._("New user registered. You are now logged in."))
                self.login_successful.emit(selected_role)
            break # Salir del bucle del generador