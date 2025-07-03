import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from config.config import DATA_DIR, DATABASE_URL
from core.utils import get_logger, hash_password, verify_password

logger = get_logger(__name__)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    _password_hash = Column(String, nullable=False) # Almacena el hash de la contraseña
    role = Column(String, default='user') # user, admin, educator, activist
    created_at = Column(DateTime, default=datetime.now)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        self._password_hash = hash_password(password)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self._password_hash)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

class ModuleSetting(Base):
    __tablename__ = 'module_settings'
    id = Column(Integer, primary_key=True)
    module_name = Column(String, nullable=False, unique=True)
    settings_json = Column(Text, nullable=False) # JSON string of module-specific settings
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<ModuleSetting(module_name='{self.module_name}')>"

class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False) # Foreign key to User
    encrypted_content = Column(Text, nullable=False)
    sentiment_analysis = Column(String) # e.g., positive, negative, neutral
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<JournalEntry(user_id={self.user_id}, created_at='{self.created_at}')>"

# Configuración de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa la base de datos y crea las tablas si no existen."""
    Base.metadata.create_all(bind=engine)
    logger.info(f"Database initialized at {DATABASE_URL}")

def get_db():
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()