"""
ChatManager: gestiona el ciclo de chat conversacional con el usuario y coordina el orquestador.
"""
from src.ia_client import IAClient
from src.langgraphflow.graph_manager import GraphManager
from langchain.memory import ConversationBufferMemory


class ChatManager:
    def __init__(self):
        pass
    
    def run(self):
        print("Bienvenido al Asistente de Inversión IA (Multiagente)")
        print("Escribe tu pregunta o 'salir' para terminar.")
        print("El sistema está preparado para hacer análisis fundamental, técnico y de noticias. Si quieres información precisa sobre una empresa, intenta proporcionar el 'ticker' o el nombre exacto de la empresa en tu pregunta.")
        chat_history = ConversationBufferMemory()
        tempaux=True
        while True:
            #question = input("\nPregunta: ")
            if tempaux:
                question = "\nPregunta: dime si es buen momento para comprar acciones de Google y Nvidia en la próxima semana y por qué"
                tempaux=False
            else:
                question = input("\nPregunta: ")

            if question.lower() == 'salir':
                print("Hasta pronto!")
                break
            #respuesta = self.orchestrator.handle_query(pregunta)
            #response = ia_client.IA_call_process_message(message=question, context=context, use_history=True)
            response  = self._initiate_graph_flow(question, chat_history)
            chat_history.save_context({"input": question}, {"output": response})
            print("\nInforme:\n", response)
    
    def _initiate_graph_flow(self, question, chat_history: ConversationBufferMemory):
        # Inicia el grafo con la pregunta del usuario
        graph = GraphManager(question,chat_history.buffer)
        response = graph.run()
        return response