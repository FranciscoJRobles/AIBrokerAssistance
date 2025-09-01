"""
Nodo Orquestador: primer nodo del grafo, usa un agente de LangChain para decidir y ejecutar tools.
"""
from typing import Dict
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from src.ia_client import IAClient
from langgraphflow.states.report_state import ReportState
from langgraphflow.states.report_state_manager import ReportStateManager

# Definición real de tools usando langchain.tools.Tool
fundamental_tool = Tool(
    name="fundamental",
    description="Análisis fundamental de empresas: ratios financieros, balances, PER, ROE, etc."
)
technical_tool = Tool(
    name="technical",
    description="Análisis técnico: indicadores, series históricas, señales como RSI, MACD, medias móviles."
)
news_tool = Tool(
    name="news",
    description="Análisis de noticias y contexto: información cualitativa, impacto de eventos y declaraciones."
)
synthesis_tool = Tool(
    name="synthesis",
    description="Síntesis e integración de resultados de los agentes anteriores para generar un informe final."
)

TOOLS = [fundamental_tool, technical_tool, news_tool, synthesis_tool]

class OrquestatorNode:
    def __init__(self, llm_client: IAClient):
        self.llm_client = llm_client
        self.tools = TOOLS        
        
    def __call__(self, state: ReportState) -> ReportState:
        state_manager = ReportStateManager(state)
        pregunta = state_manager.get_user_question()  # O ajusta según cómo guardes la pregunta
        chat_history = state_manager.get_chat_history()
        result = self.call_IA_get_nodes_route(pregunta, chat_history)
        state_manager.set_nodes_route(result)
                
        return state

    def call_IA_get_nodes_route(self, pregunta: str, chat_history: str = "") -> list:
        """
        Llama al LLM y le plantea la pregunta y el trabajo multiagente.
        El modelo debe devolver una lista de strings con los nodos a recorrer.
        """
        try:
            
            json_structure = {
                "nodes_route": [],  # Ejemplo: ['fundamental', 'technical', 'synthesis']     
                "empresas": [  # Lista de objetos con nombre y ticker
                    # {"nombre": "Apple", "ticker": "AAPL"},
                    # {"nombre": "Banco Santander", "ticker": "SAN"}
                ],
                "sector": None,
                "periodo": "próxima semana",
                "tipo_analisis": "proyección_subida",
                # ...otros campos relevantes
            }
            
            tools_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
            system_prompt = f"""
                Devuelve SIEMPRE un JSON puro, válido y en una sola línea, sin explicaciones ni texto adicional fuera del JSON.

                Eres el orquestador de un sistema multiagente de análisis bursátil. Vas a recibir la pregunta de un usuario, que puede ser amplia o específica, y tienes que extraer la siguiente información en el JSON:

                - nodes_route: Lista de nodos a ejecutar en orden, según el análisis necesario para responder a la pregunta. El último nodo debe ser siempre 'synthesis', que genera el informe final. Ejemplo: ['fundamental', 'technical', 'synthesis']. Aquí tienes la lista de nodos disponibles y sus descripciones:\n{tools_descriptions}\n
                - empresas: Lista de objetos, cada uno con el nombre y el ticker de la empresa relevante para la pregunta. Ejemplo: [{{"nombre": "Apple", "ticker": "AAPL"}}, {{"nombre": "Banco Santander", "ticker": "SAN"}}]. Si no se menciona ninguna empresa concreta, deja la lista vacía y los nodos posteriores buscarán en el universo completo.
                - sector: Sector económico relevante para la pregunta (por ejemplo, 'tecnología', 'banca', 'energía'). Si no se especifica, pon null.
                - periodo: Periodo temporal relevante para el análisis (por ejemplo, 'próxima semana', 'último año', '2025'). Si no se menciona, pon null.
                - tipo_analisis: Tipo de análisis solicitado por el usuario (por ejemplo, 'proyección_subida', 'comparación', 'recomendación', 'análisis_fundamental'). Extrae la intención principal de la pregunta.
                - Puedes añadir otros campos relevantes si la pregunta lo requiere (por ejemplo, país, mercado, etc.).

                En función de la pregunta y el contexto, decide la ruta óptima de nodos a ejecutar.
                Usa el histórico para tener en cuenta la información que ya dispones para evitar hacer búsquedas repetidas si se puede reusar esa información. Si consideras que para responder a la pregunta te basta con la información del histórico, la ruta de nodos debe ser solo ['synthesis'].

                Recuerda: SOLO devuelve el JSON estrictamente puro, válido y en una sola linea, sin explicaciones ni texto adicional.
            """
            user_prompt = f"""
                El histórico del chat, si existe, es:\n{chat_history}\n
                La pregunta del usuario es: '{pregunta}'\n\n"
                
            """
            # Llama al LLM
            llm_response = self.llm_client.IA_call_process_message(user_prompt, system_prompt)
            return llm_response
        except Exception:
            print("OrquestatorNode: Error al interpretar la respuesta del LLM")
            
 



# Helper para el grafo

def orquestator_node(state: ReportState) -> ReportState:
    node = OrquestatorNode()
    return node(state)


