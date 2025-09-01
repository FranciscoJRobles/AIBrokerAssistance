

from typing import List, TypedDict


class ReportState(TypedDict):
    """Estado que contiene toda la información necesaria para generar un reporte/informe de broker."""
    
    # initial data
    ChatHistory: str  # Historial de conversación
    user_question: str  # Pregunta del usuario
    
    nodes_route: List[str]
    
    final_response: str  # Respuesta final generada