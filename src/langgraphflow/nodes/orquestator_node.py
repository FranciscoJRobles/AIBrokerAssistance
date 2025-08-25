"""
Nodo Orquestador: primer nodo del grafo, usa un LLM para decidir el agente/tool a activar.
"""
from typing import Dict, List
from src.ia_client import IAClient

# Definición de tools/agentes disponibles
TOOLS = [
    {
        "name": "fundamental",
        "description": "Análisis fundamental de empresas: ratios financieros, balances, PER, ROE, etc.",
    },
    {
        "name": "technical",
        "description": "Análisis técnico: indicadores, series históricas, señales como RSI, MACD, medias móviles.",
    },
    {
        "name": "news",
        "description": "Análisis de noticias y contexto: información cualitativa, impacto de eventos y declaraciones.",
    },
    {
        "name": "synthesis",
        "description": "Síntesis e integración de resultados de los agentes anteriores para generar un informe final.",
    },
]

# Instancia del cliente LLM (puedes parametrizarlo si lo necesitas)
llm_client = IAClient()


def orquestator_node(input_data: Dict) -> Dict:
    """
    Recibe el input del usuario, consulta el LLM y decide el agente/tool a activar.
    Devuelve un diccionario con la decisión y el input enriquecido.
    """
    pregunta = input_data.get("pregunta", "")
    # Construye el prompt para el LLM
    tools_descriptions = "\n".join([f"- {tool['name']}: {tool['description']}" for tool in TOOLS])
    prompt = (
        f"Eres un orquestador multiagente de inversión."
        f" El usuario ha preguntado: '{pregunta}'."
        f" Dispones de los siguientes agentes/tools:\n{tools_descriptions}\n"
        f"¿Qué agente/tool deberías activar primero para responder mejor a la pregunta?"
        f" Responde solo con el nombre del agente/tool más adecuado."
    )
    # Llama al LLM para decidir el agente
    decision = llm_client.IA_call_process_message(prompt).strip().lower()
    # Valida la decisión
    if decision not in [tool["name"] for tool in TOOLS]:
        decision = "fundamental"  # Por defecto si el LLM no responde bien
    return {
        "pregunta": pregunta,
        "decision": decision,
        "contexto": input_data.get("contexto", "")
    }
