"""
Nodo/agente de análisis fundamental para el grafo LangGraph.
"""
from langgraphflow.states.report_state import ReportState
from langgraphflow.states.report_state_manager import ReportStateManager

class FundamentalNode:

    def __init__(self):
        pass

    def get_fundamental_result(self, pregunta: str, chat_history: str = "") -> dict:
        """
        Recopila información fundamental usando lógica algorítmica tradicional (APIs, cálculos, etc).
        Devuelve un dict con los datos relevantes.
        """
        # Aquí iría la lógica real: consulta a APIs, cálculos, etc.
        # Simulación de datos:
        resultado = {
            "empresa": "EjemploCorp",
            "PER": 15.2,
            "ROE": 8.7,
            "deuda": 12000000,
            "comentario": f"Datos fundamentales recopilados para la pregunta: '{pregunta}'"
        }
        return resultado

    def __call__(self, state: ReportState) -> ReportState:
        state_manager = ReportStateManager(state)
        pregunta = state_manager.get_user_question()
        chat_history = state_manager.get_chat_history()

        resultado = self.get_fundamental_result(pregunta, chat_history)
        state_manager.set_fundamental_result(resultado)
        return state

# Helper para el grafo
def fundamental_node(state: ReportState) -> ReportState:
    node = FundamentalNode()
    return node(state)