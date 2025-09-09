"""
Punto de entrada del Asistente de Inversión IA (Multiagente)
"""
from src.chat_manager import ChatManager
from utils.env_loader import define_custom_env_variables, get_env_variable


def main():
    env = get_env_variable("ENV", "local")
    if env == "local":
        define_custom_env_variables()
    
    chat = ChatManager()
    chat.run()

if __name__ == "__main__":
    main()
