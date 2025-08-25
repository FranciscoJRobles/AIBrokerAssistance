from typing import TypedDict

class ReportState(TypedDict):
    ConversationHistory: str

class ReportStateManager:
    def __init__(self, state: ReportState):
        self.state = state

    def get_conversation_history(self) -> str:
        return self.state.get('ConversationHistory', '')

    def set_conversation_history(self, value: str):
        self.state['ConversationHistory'] = value
