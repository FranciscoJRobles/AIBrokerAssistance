class NodeTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
fundamental_tool = NodeTool(
    name="fundamental",
    description="Análisis fundamental de empresas: ratios financieros, balances, PER, ROE, etc. Siempre que se ejecuta este nodo  devuelve la misma información para todas las empresas indicadas."
)
technical_tool = NodeTool(
    name="technical",
    description="Análisis técnico: indicadores, series históricas, señales como RSI, MACD, medias móviles. Siempre que se ejecuta este nodo  devuelve la misma información para todas las empresas indicadas."
)
news_tool = NodeTool(
    name="news",
    description="Análisis de noticias y contexto: información cualitativa, impacto de eventos y declaraciones de personajes influyentes."
)
synthesis_tool = NodeTool(
    name="synthesis",
    description="Síntesis e integración de resultados de los agentes anteriores para generar un informe final. Siempre será el último nodo que se ejecute."
)

TOOLS = [fundamental_tool, technical_tool, news_tool, synthesis_tool]

def get_tools_list():
    return TOOLS