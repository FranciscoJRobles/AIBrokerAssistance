"""
ChatManager: gestiona el ciclo de chat conversacional con el usuario y coordina el orquestador.
"""
from src.ia_client import IAClient
from src.langgraph.graph_manager import GraphManager

class ChatManager:
    def __init__(self):
        self.graph = GraphManager()

    def run(self):
        print("Bienvenido al Asistente de Inversión IA (Multiagente)")
        print("Escribe tu pregunta o 'salir' para terminar.")
        ia_client = IAClient()
        initial_chat = True
        while True:
            if initial_chat:
                context = self.get_initial_prompt()
                initial_chat = False
            else:
                context = None  
            question = input("\nPregunta: ")
            if question.lower() == 'salir':
                print("Hasta pronto!")
                break
            #respuesta = self.orchestrator.handle_query(pregunta)
            response = ia_client.IA_call_process_message(message=question, context=context, use_history=True)
            print("\nInforme:\n", response)

    def get_initial_prompt(self):
        return "Eres un asistente financiero experto. Responde de manera clara y concisa."