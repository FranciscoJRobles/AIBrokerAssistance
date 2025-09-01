

from typing import List, TypedDict


class ReportState(TypedDict):
    """Estado que contiene toda la información necesaria para generar un reporte/informe de broker."""
    
    # initial data
    ChatHistory: str  # Historial de conversación
    user_question: str  # Pregunta del usuario
    
    nodes_route: List[str]
    companies: List[dict]  # Lista de empresas con nombre y ticker
    sector: str  # Sector económico relevante
    period: str  # Periodo temporal relevante
    analysis_type: str  # Tipo de análisis solicitado
    # responses from nodes
    fundamental_result: str
    technical_result: str
    news_result: str
    
    final_response: str  # Respuesta final generada