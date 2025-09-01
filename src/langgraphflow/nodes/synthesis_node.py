"""
Nodo/agente de síntesis para el grafo LangGraph.
"""
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
from src.ia_client import IAClient, IAProfilesEnum  # Asumiendo que tienes un cliente LLM

class SynthesisNode:
    def __init__(self):
        self.llm_client = IAClient(profile=IAProfilesEnum.RESUME)

    def __call__(self, state: ReportState) -> ReportState:
        state_manager = ReportStateManager(state)
        # Recopila toda la información relevante del estado
        user_question = state_manager.get_user_question()
        chat_history = state_manager.get_chat_history()
        companies = state_manager.get_companies()
        sector = state_manager.get_sector()
        period = state_manager.get_period()
        analysis_type = state_manager.get_analysis_type()
        fundamental_result = state_manager.get_fundamental_result()
        technical_result = state_manager.get_technical_result()
        news_result = state_manager.get_news_result()

        # Construye el prompt para el LLM
        final_report = self.call_IA_synthesis_information(
            user_question, companies, sector, period, analysis_type,
            fundamental_result, technical_result, news_result, chat_history
        )

        # Guarda el informe en el estado
        state_manager.set_final_response(final_report)
        return state

    def call_IA_synthesis_information(
        self, user_question, companies, sector, period, analysis_type,
        fundamental_result, technical_result, news_result, chat_history
    ):
        # Puedes personalizar el prompt para que el LLM integre y explique todos los resultados
        system_prompt = f"""
            Eres un asistente financiero profesional. Vas a recibir en el mensaje del usuario toda la información relevante para generar un informe de síntesis: 
            la pregunta original, las empresas analizadas, el sector, el periodo, el tipo de análisis, los resultados de los agentes (fundamental, técnico, noticias) y el histórico de la conversación. 
            Ten en cuenta que no siempre recibirás información en todos los campos, ya que los nodos ejecutados pueden variar según la consulta del usuario. 
            Usa el histórico, si existe y es relevante, para contextualizar la respuesta, añadir información previa o evitar repeticiones innecesarias.
            Tu tarea es integrar todos los datos disponibles y generar un informe final claro, profesional y útil para el usuario, explicando los resultados de forma comprensible y evitando repeticiones innecesarias.
        """
        
        user_prompt = f"""
            Pregunta o comentario del usuario: {user_question}
            Empresas analizadas: {companies}
            Sector: {sector}
            Periodo: {period}
            Tipo de análisis: {analysis_type}

            Resultados de análisis fundamental:
            {fundamental_result}

            Resultados de análisis técnico:
            {technical_result}

            Resultados de análisis de noticias:
            {news_result}

            Histórico de la conversación:
            {chat_history}
        """    
        
        
        llm_response = self.llm_client.IA_call_process_message(user_prompt, system_prompt)
        return llm_response
        
    
    

# Helper para el grafo
def synthesis_node(state: ReportState) -> ReportState:
    node = SynthesisNode()
    return node(state)