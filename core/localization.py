import gettext
import os
from config.config import LOCALIZATION_DIR

_translators = {}

def get_translator(lang):
    if lang not in _translators:
        try:
            # Asegurarse de que el dominio sea consistente con la estructura de gettext
            # Por ejemplo, si los archivos .mo están en localization/es/LC_MESSAGES/messages.mo
            # el dominio sería 'messages'
            localedir = LOCALIZATION_DIR
            lang_dir = os.path.join(localedir, lang, 'LC_MESSAGES')
            if not os.path.exists(lang_dir):
                os.makedirs(lang_dir)

            # Crear un archivo .po vacío si no existe para que gettext no falle
            po_file = os.path.join(localedir, lang, 'LC_MESSAGES', 'messages.po')
            if not os.path.exists(po_file):
                with open(po_file, 'w') as f:
                    f.write('# Empty PO file for ' + lang + '\n')

            # Compilar el archivo .po a .mo (si no existe o es más antiguo)
            mo_file = os.path.join(localedir, lang, 'LC_MESSAGES', 'messages.mo')
            if not os.path.exists(mo_file) or os.path.getmtime(po_file) > os.path.getmtime(mo_file):
                # Usar msgfmt para compilar el .po a .mo
                # Esto requiere que gettext esté instalado en el sistema
                try:
                    import subprocess
                    subprocess.run(['msgfmt', po_file, '-o', mo_file], check=True)
                except FileNotFoundError:
                    print(f"Advertencia: msgfmt no encontrado. No se pudo compilar {po_file}. La internacionalización podría no funcionar correctamente.")
                except subprocess.CalledProcessError as e:
                    print(f"Error al compilar {po_file}: {e}")

            # Cargar el traductor
            t = gettext.translation('messages', localedir=localedir, languages=[lang], fallback=True)
            t.install()
            _translators[lang] = t.gettext
        except Exception as e:
            print(f"Error al cargar la traducción para {lang}: {e}. Usando traductor predeterminado.")
            _translators[lang] = gettext.gettext # Fallback a gettext predeterminado
    return _translators[lang]

# Inicializar el traductor por defecto
_ = get_translator('en')
