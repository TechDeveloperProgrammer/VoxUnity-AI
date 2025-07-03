import unittest
import os
import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from core.database import init_db, get_db, User, ModuleSetting, JournalEntry
from core.utils import load_json_file, save_json_file, get_timestamp, hash_password, verify_password, create_access_token, decode_access_token
from config.config import DATA_DIR, SECRET_KEY

class TestCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Asegurarse de que el directorio de datos exista para la DB de prueba
        os.makedirs(DATA_DIR, exist_ok=True)
        # Inicializar la DB para las pruebas
        init_db()

    def setUp(self):
        # Limpiar la DB antes de cada prueba
        db: Session
        for db in get_db():
            db.query(User).delete()
            db.query(ModuleSetting).delete()
            db.query(JournalEntry).delete()
            db.commit()
            break

    def test_user_creation_and_password_hashing(self):
        db: Session
        for db in get_db():
            new_user = User(username="testuser", password="plainpassword", role="user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            self.assertIsNotNone(new_user.id)
            self.assertEqual(new_user.username, "testuser")
            self.assertTrue(verify_password("plainpassword", new_user._password_hash))
            self.assertFalse(verify_password("wrongpassword", new_user._password_hash))
            break

    def test_module_setting_storage(self):
        db: Session
        for db in get_db():
            settings_data = {"setting1": "value1", "setting2": 123}
            new_setting = ModuleSetting(module_name="mod-test", settings_json=json.dumps(settings_data))
            db.add(new_setting)
            db.commit()
            db.refresh(new_setting)
            self.assertIsNotNone(new_setting.id)
            self.assertEqual(json.loads(new_setting.settings_json), settings_data)
            break

    def test_journal_entry_storage(self):
        db: Session
        for db in get_db():
            # Crear un usuario primero
            new_user = User(username="journaluser", password="pass", role="user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            encrypted_content = "encrypted_test_content"
            sentiment = "neutral"

            new_entry = JournalEntry(
                user_id=new_user.id,
                encrypted_content=encrypted_content,
                sentiment_analysis=sentiment
            )
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)

            self.assertIsNotNone(new_entry.id)
            self.assertEqual(new_entry.user_id, new_user.id)
            self.assertEqual(new_entry.encrypted_content, encrypted_content)
            self.assertEqual(new_entry.sentiment_analysis, sentiment)
            break

    def test_load_save_json_file(self):
        test_file = os.path.join(DATA_DIR, "test_data.json")
        test_data = {"key": "value", "number": 123}

        # Guardar
        success = save_json_file(test_file, test_data)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(test_file))

        # Cargar
        loaded_data = load_json_file(test_file)
        self.assertEqual(loaded_data, test_data)

        # Limpiar
        os.remove(test_file)

    def test_get_timestamp(self):
        timestamp = get_timestamp()
        self.assertIsInstance(timestamp, str)
        # Verificar formato básico (ej. YYYY-MM-DD HH:MM:SS)
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    def test_jwt_creation_and_decoding(self):
        payload = {"user_id": 1, "username": "testuser", "role": "admin"}
        token = create_access_token(payload, SECRET_KEY, expires_delta=timedelta(minutes=1))
        self.assertIsInstance(token, str)

        decoded_payload = decode_access_token(token, SECRET_KEY)
        self.assertIsNotNone(decoded_payload)
        self.assertEqual(decoded_payload["user_id"], payload["user_id"])
        self.assertEqual(decoded_payload["username"], payload["username"])
        self.assertEqual(decoded_payload["role"], payload["role"])

    def test_jwt_expiration(self):
        payload = {"user_id": 1, "username": "testuser"}
        token = create_access_token(payload, SECRET_KEY, expires_delta=timedelta(seconds=-1)) # Token expirado

        decoded_payload = decode_access_token(token, SECRET_KEY)
        self.assertIsNone(decoded_payload)

if __name__ == '__main__':
    unittest.main()