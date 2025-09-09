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


def define_custom_env_variables():
    """
    Define variables de entorno personalizadas en tiempo de ejecución.
    custom_vars: dict con pares clave-valor para definir en el entorno.
    """
    os.environ['SSL_CERT_FILE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
    os.environ['REQUESTS_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
    os.environ['CURL_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"