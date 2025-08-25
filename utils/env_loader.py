# Utilidad para cargar variables de entorno
from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variable(key: str, default=None, cast_type=None):
    value = os.getenv(key, default)
    if cast_type and value is not None:
        try:
            return cast_type(value)
        except Exception:
            return default
    return value
