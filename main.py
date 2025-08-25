"""
Punto de entrada del Asistente de Inversión IA (Multiagente)
"""
from src.chat_manager import ChatManager

def main():
    chat = ChatManager()
    chat.run()

if __name__ == "__main__":
    main()
