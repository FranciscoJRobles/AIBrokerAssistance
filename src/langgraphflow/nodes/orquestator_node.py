"""
Nodo Orquestador: primer nodo del grafo, usa un agente de LangChain para decidir y ejecutar tools.
"""
import json
from typing import Dict
from langchain.tools import Tool
from src.ia_client import IAClient, IAProfilesEnum
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
from src.langgraphflow.utils.node_tool import NodeTool, get_tools_list
from utils.utils import json_clean_response

class OrquestatorNode:
    def __init__(self):
        self.llm_client = IAClient(profile=IAProfilesEnum.ANALYST)
        self.tools = get_tools_list()
        
    def __call__(self, state: ReportState) -> ReportState:
        try:
            state_manager = ReportStateManager(state)
            pregunta = state_manager.get_user_question()  # O ajusta según cómo guardes la pregunta
            chat_history = state_manager.get_chat_history()
            result = self.call_IA_extract_question_information(pregunta, chat_history)
            state_manager.set_nodes_route(result.get("nodes_route", []))
            state_manager.set_companies(result.get("companies", []))
            state_manager.set_sector(result.get("sector", ""))
            state_manager.set_period(result.get("period", ""))
            state_manager.set_analysis_type(result.get("analysis_type", ""))
                    
            return state
        except Exception as e:
            print(f"OrquestatorNode: Error al ejecutar el nodo: {e}")
            return state

    def call_IA_extract_question_information(self, pregunta: str, chat_history: str = "") -> list:
        """
        Llama al LLM y le plantea la pregunta y el trabajo multiagente.
        El modelo debe devolver una lista de strings con los nodos a recorrer.
        """
        try:
            
            json_structure = {
                "nodes_route": [],  # Ejemplo: ['fundamental', 'technical', 'synthesis']     
                "companies": [  # Lista de objetos con nombre y ticker
                    {"name": "Apple", "ticker": "AAPL"},
                    {"name": "Banco Santander", "ticker": "SAN"}
                ],
                "sector": None,
                "period": "próxima semana",
                "analysis_type": "proyección_subida",
                # ...otros campos relevantes
            }
            estructura_json_str = json.dumps(json_structure, ensure_ascii=False)
            tools_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
            system_prompt = f"""
                Devuelve SIEMPRE un JSON plano, puro y estríctamente válido en una sola línea, sin explicaciones ni texto adicional fuera del JSON.

                Eres el orquestador de un sistema multiagente de análisis bursátil. Vas a recibir la pregunta de un usuario, que puede ser amplia o específica, y tienes que extraer la siguiente información en el JSON:

                - nodes_route: Lista de nodos a ejecutar en orden, según el análisis necesario para responder a la pregunta. El último nodo debe ser siempre 'synthesis', que genera el informe final. Ejemplo: ['fundamental', 'technical', 'synthesis']. Aquí tienes la lista de nodos disponibles y sus descripciones:\n{tools_descriptions}\n
                - companies: Lista de objetos, cada uno con el nombre y el ticker de la empresa relevante para la pregunta. Ejemplo: [{{"nombre": "Apple", "ticker": "AAPL"}}, {{"nombre": "Banco Santander", "ticker": "SAN"}}]. Si no se menciona ninguna empresa concreta, deja la lista vacía y los nodos posteriores buscarán en el universo completo.
                - sector: Sector económico relevante para la pregunta (por ejemplo, 'tecnología', 'banca', 'energía'). Si no se especifica, pon null.
                - period: Periodo temporal relevante para el análisis (por ejemplo, 'próxima semana', 'último año', '2025'). Si no se menciona, pon null.
                - analysis_type: Tipo de análisis solicitado por el usuario (por ejemplo, 'proyección_subida', 'comparación', 'recomendación', 'análisis_fundamental'). Extrae la intención principal de la pregunta.
                - Puedes añadir otros campos relevantes si la pregunta lo requiere (por ejemplo, país, mercado, etc.).
                
                Usa el histórico para tener en cuenta la información que ya dispones para evitar hacer búsquedas repetidas si se puede reusar esa información. Si consideras que para responder a la pregunta te basta con la información del histórico, la ruta de nodos debe ser solo ['synthesis'].
                La estructura JSON de salida que debes seguir es esta:\n {estructura_json_str}

                Recuerda: SOLO  Devuelve SIEMPRE un JSON plano, puro y estríctamente válido en una sola línea, sin explicaciones ni texto adicional.
            """
            user_prompt = f"""
                El histórico del chat, si existe, es:\n{chat_history}\n
                La pregunta del usuario es: '{pregunta}'\n\n"
                
            """
            # Llama al LLM
            llm_response = self.llm_client.IA_call_process_message(user_prompt, system_prompt)
            data = json.loads(json_clean_response(llm_response))
            return data
        except Exception:
            print("OrquestatorNode: Error al interpretar la respuesta del LLM")
            
 



# Helper para el grafo

def orquestator_node(state: ReportState) -> ReportState:
    node = OrquestatorNode()
    return node(state)


