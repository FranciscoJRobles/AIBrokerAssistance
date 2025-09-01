from src.langgraphflow.states.report_state import ReportState


class ReportStateManager:
    def __init__(self, state: ReportState):
        self.state = state

    def get_chat_history(self) -> str:
        return self.state.get('ChatHistory', '')
    def set_chat_history(self, value: str):
        self.state['ChatHistory'] = value
        
    def get_user_question(self) -> str:
        return self.state.get('user_question', '')
    def set_user_question(self, value: str):
        self.state['user_question'] = value

    # datos del nodo orquestador
    def get_nodes_route(self) -> list:
        return self.state.get('nodes_route', [])
    def set_nodes_route(self, value: list):
        self.state['nodes_route'] = value

    def get_companies(self) -> list:
        return self.state.get('companies', [])
    def set_companies(self, value: list):
        self.state['companies'] = value

    def get_sector(self) -> str:
        return self.state.get('sector', '')
    def set_sector(self, value: str):
        self.state['sector'] = value

    def get_period(self) -> str:
        return self.state.get('period', '')
    def set_period(self, value: str):
        self.state['period'] = value

    def get_analysis_type(self) -> str:
        return self.state.get('analysis_type', '')
    def set_analysis_type(self, value: str):
        self.state['analysis_type'] = value
        
    # -------------
    
    def get_fundamental_result(self) -> str:
        return self.state.get('fundamental_result', '')
    def set_fundamental_result(self, value: str):
        self.state['fundamental_result'] = value
    
    def get_technical_result(self) -> str:
        return self.state.get('technical_result', '')
    def set_technical_result(self, value: str):
        self.state['technical_result'] = value
        
    def get_news_result(self) -> str:
        return self.state.get('news_result', '')
    def set_news_result(self, value: str):
        self.state['news_result'] = value
    
    def get_final_response(self) -> str:
        return self.state.get('final_response', '')
    def set_final_response(self, value: str):
        self.state['final_response'] = value