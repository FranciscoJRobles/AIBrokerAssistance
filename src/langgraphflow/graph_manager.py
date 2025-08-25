"""
GraphManager: Define el grafo principal y la orquestación multiagente con LangGraph.
"""
from langgraph.graph import StateGraph, END
from src.langgraphflow.nodes.fundamental_node import fundamental_node
from src.langgraphflow.nodes.synthesis_node import synthesis_node

class GraphManager:
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph()
        # Registrar nodos/agentes
        graph.add_node("fundamental", fundamental_node)
        graph.add_node("synthesis", synthesis_node)
        # Ejemplo: conexión secuencial
        graph.add_edge("fundamental", "synthesis")
        # Ejemplo: conexión condicional (placeholder)
        # graph.add_conditional_edge("fundamental", self.condicion_agente, {"synthesis": synthesis_node})
        # Definir el nodo de entrada y salida
        graph.set_entry_node("fundamental")
        graph.set_exit_node("synthesis")
        return graph

    def run(self, input_data):
        # Ejecuta el grafo con el input del usuario
        result = self.graph.run(input_data)
        return result

    # Ejemplo de función condicional para decidir el siguiente nodo
    def condicion_agente(self, input_data):
        # Aquí puedes analizar el input y decidir el siguiente nodo
        if "sintetizar" in str(input_data).lower():
            return "synthesis"
        return "synthesis"  # Por defecto
