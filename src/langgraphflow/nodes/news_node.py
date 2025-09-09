"""
Nodo/agente de análisis de noticias para el grafo LangGraph.
"""
import ast
import json
from utils.env_loader import get_env_variable
import requests, os
from bs4 import BeautifulSoup
from langchain_community.tools.searchapi.tool import SearchAPIResults, SearchAPIRun
from langchain_community.utilities import SearchApiAPIWrapper
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager

class NewsNode:

    def __init__(self):
        serpapi_api_key = get_env_variable("SEARCHAPI_API_KEY")
        google_api_wrapper = SearchApiAPIWrapper(engine="google_news", searchapi_api_key=serpapi_api_key)  # Puedes cambiar el motor aquí
        self.serpapi = SearchAPIResults(api_wrapper=google_api_wrapper)

    def __call__(self, state: ReportState) -> ReportState:
        try:
            state_manager = ReportStateManager(state)
            companies = state_manager.get_companies()  # Lista de dicts con nombre y ticker
            global_query = state_manager.get_global_news_query()
            # TODO: comprobar si global_query tiene datos y hacer una búsqueda preliminar de empresas relevantes, luego añadirlas a companies y hacer la búsqueda completa.
            resultado = self.get_companies_news(companies)
            # TODO contemplar la posibilidad de hacer un filtrado preliminar de la lista de urls extraida de la búsqueda con el motor de búsqueda, ya sea con LLM u otro método.
            
            state_manager.set_news_result(resultado)
            return state
        except Exception as e:
            print(f"NewsNode: Error al ejecutar el nodo: {e}")
            state_manager.set_news_result({"error": str(e)})
            return state

    def get_companies_news(self, companies) -> dict:
        results = []
        for company in companies:
            nombre = company.get("name")
            ticker = company.get("ticker")
            query = company.get("news_query")
            try:
                news_list = self.search_news_serpapi(query)
            except Exception as e:
                print(f"SerpAPI error: {e}. Usando motor de búsqueda de respaldo.")
                # TODO: Buscar con motor de búsqueda de respaldo
                #news_list = self.search_news_duckduckgo(query)
            result = {
                "nombre": nombre,
                "ticker": ticker,
                "noticias": news_list,
                "comentario": f"Noticias relevantes de {nombre} ({ticker}) extraídas correctamente."
            }
            results.append(result)
        return results

    def search_news_serpapi(self, query):
        results = self.serpapi.run(query)
        result_dict = ast.literal_eval(results)
        news_list = []
        for item in result_dict.get("organic_results", []):
            news_list.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "source": item.get("source"),
                "date": item.get("date"),
                "snippet": item.get("snippet"),
            })
        return news_list

def scrape_url(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Prueba selectores típicos
        main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content') # TODO mejorar selectores
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        # Opcional: Limpiar saltos de línea y espacios extra
        return ' '.join(text.split())
    except Exception as e:
        print (f"Error scraping {url}: {e}")

# Helper para el grafo
def news_node(state: ReportState) -> ReportState:
    node = NewsNode()
    return node(state)




# PÁGINAS FIABLES DE NOTICIAS:
# Bloomberg (https://www.bloomberg.com/)
# Noticias financieras globales, datos de mercado en tiempo real, análisis y reportajes de gran influencia.

# Reuters (https://www.reuters.com/finance)
# Agencia de noticias muy respetada, actualizaciones rápidas sobre empresas y mercados.

# Financial Times (FT) (https://www.ft.com/)
# Cobertura profunda de mercados, empresas y economía internacional.

# The Wall Street Journal (WSJ) (https://www.wsj.com/)
# Referencia clave en información corporativa, economía y finanzas.

# CNBC (https://www.cnbc.com/world/)
# Noticias financieras con foco en EE.UU. pero con cobertura global.

# MarketWatch (https://www.marketwatch.com/)
# Noticias sobre mercados, cotizaciones y análisis de inversión.