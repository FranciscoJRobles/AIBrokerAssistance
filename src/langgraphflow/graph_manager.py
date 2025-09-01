"""
GraphManager: Define el grafo principal y la orquestación multiagente con LangGraph.
"""
import uuid
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
from src.langgraphflow.nodes.fundamental_node import fundamental_node
from src.langgraphflow.nodes.synthesis_node import synthesis_node
from src.langgraphflow.nodes.orquestator_node import orquestator_node
from sqlalchemy.orm import Session


class GraphManager:
    def __init__(self, question, chat_history):
        self.checkpointer = MemorySaver()  # Para persistir estado entre ejecuciones
        self.question = question
        self.chat_history = chat_history        
        self.graph = self._build_graph()
        
        #self.db_session = Session()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ReportState)
        # Registrar nodos/agentes
        graph.add_node("orquestator", lambda state: orquestator_node(state))
        graph.add_node("fundamental", lambda state: fundamental_node(state))
        graph.add_node("synthesis", lambda state: synthesis_node(state))
        
        graph.set_entry_point("orquestator")
        
        graph.add_conditional_edges("orquestator", lambda state: next_node_selector(state), {
            "fundamental": "fundamental"
        })
        
        graph.add_conditional_edges("fundamental", lambda state: next_node_selector(state), {
            "synthesis": "synthesis"
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
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}
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
        return state['nodes_route'].pop(0)
    return 'synthesis'