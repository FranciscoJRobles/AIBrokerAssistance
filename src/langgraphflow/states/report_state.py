

from typing import TypedDict


class ReportState(TypedDict):
    """Estado que contiene toda la información necesaria para generar un reporte/informe de broker."""
    
    ConversationHistory: str  # Historial de conversación