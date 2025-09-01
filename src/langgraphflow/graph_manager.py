"""
GraphManager: Define el grafo principal y la orquestación multiagente con LangGraph.
"""
from langgraph.graph import StateGraph, END
from ia_client import IAClient
from langgraphflow.states.report_state import ReportState
from langgraph.checkpoint.memory import MemorySaver
from langgraphflow.states.report_state_manager import ReportStateManager
from src.langgraphflow.nodes.fundamental_node import fundamental_node
from src.langgraphflow.nodes.synthesis_node import synthesis_node
from src.langgraphflow.nodes.orquestator_node import orquestator_node
from sqlalchemy.orm import Session


class GraphManager:
    def __init__(self, question, chat_history):
        self.checkpointer = MemorySaver()  # Para persistir estado entre ejecuciones
        self.llm_client = IAClient()
        self.nodes = ['fundamental','synthesis', 'end']
        self.question = question
        self.chat_history = chat_history        
        self.graph = self._build_graph()
        
        #self.db_session = Session()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ReportState)
        # Registrar nodos/agentes
        graph.add_node("orquestator", orquestator_node)
        graph.add_node("fundamental", fundamental_node)
        graph.add_node("synthesis", synthesis_node)
        
        graph.set_entry_point("orquestator")
        
        graph.add_conditional_edge("orquestator", next_node_selector, {
            "fundamental": fundamental_node
        })
        
        graph.add_conditional_edge("fundamental", next_node_selector, {
            "synthesis": synthesis_node
        })
        
        graph.add_edge("synthesis", END)
        
        return graph.compile(checkpointer=self.checkpointer)

    def run(self):
        # Ejecuta el grafo con el input del usuario
        try:
            initial_state : ReportState = {
                "ChatHistory": self.chat_history,
                "user_question": self.question,
                "final_response": ""
            }
            config = {"configurable": {"question": {self.question}}}
            state = self.graph.invoke(initial_state, config)
            state_manager = ReportStateManager(state)
            return state_manager.get_final_response()
        except Exception as e:
            print(f"GraphManager: Error al ejecutar el grafo: {e}")
            return "Error: Lo siento, ha ocurrido un error en el sistema al procesar tu solicitud."

def next_node_selector(state):
    # Devuelve el siguiente nodo de la lista, o 'synthesis' si no quedan
    state_manager = ReportStateManager(state)
    if state_manager.get_nodes_route():
        return state['next_nodes'].pop(0)
    return 'synthesis'