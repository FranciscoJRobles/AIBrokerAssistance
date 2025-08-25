"""
Orquestador: gestiona el flujo entre agentes y la integración de respuestas.
"""
from src.agents.fundamental_agent import FundamentalAgent
from src.agents.synthesis_agent import SynthesisAgent

class Orchestrator:
    def __init__(self):
        self.fundamental_agent = FundamentalAgent()
        self.synthesis_agent = SynthesisAgent()

    def handle_query(self, pregunta: str) -> str:
        # MVP: solo agente fundamental y síntesis
        datos_fundamental = self.fundamental_agent.analyze(pregunta)
        informe = self.synthesis_agent.summarize(pregunta, datos_fundamental)
        return informe
