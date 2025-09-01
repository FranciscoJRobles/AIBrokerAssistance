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
        chat_history = ConversationBufferMemory()
        while True:
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
        graph.run()
        input_data = {"question": question}
        response = self.graph.run(input_data)
        return response