"""
Nodo/agente de análisis fundamental para el grafo LangGraph.
"""
import os

import certifi
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
import yfinance as yf

os.environ['SSL_CERT_FILE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
os.environ['REQUESTS_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
os.environ['CURL_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"

class FundamentalNode:

    def __init__(self):
        pass

    def __call__(self, state: ReportState) -> ReportState:
        try:
            state_manager = ReportStateManager(state)
            companies = state_manager.get_companies()  # Lista de dicts con nombre y ticker

            resultado = self.get_fundamental_result(companies)
            state_manager.set_fundamental_result(resultado)
            return state
        except Exception as e:
            print(f"FundamentalNode: Error al ejecutar el nodo: {e}")
            state_manager.set_fundamental_result({"error": str(e)})
            return state


    def get_fundamental_result(self, companies) -> dict:
        """
        Recopila información fundamental usando yfinance (puedes añadir otras APIs).
        Devuelve un dict con los datos relevantes por empresa.
        """
        results = []
        for company in companies:
            ticker = company.get("ticker")
            nombre = company.get("nombre")
            if not ticker:
                continue
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                result = {
                    "nombre": nombre,                # Nombre de la empresa (ej: "Apple")
                    "ticker": ticker,                # Ticker bursátil (ej: "AAPL")
                    "PER": info.get("trailingPE"),   # Price/Earnings Ratio (relación precio-beneficio)
                    "ROE": info.get("returnOnEquity"), # Return on Equity (rentabilidad sobre recursos propios)
                    "deuda": info.get("totalDebt"),  # Deuda total de la empresa
                    "sector": info.get("sector"),    # Sector económico al que pertenece la empresa
                    "comentario": f"Datos fundamentales de {nombre} ({ticker}) extraídos correctamente."
                    # --- Otros datos útiles que puedes extraer ---
                    # "marketCap": info.get("marketCap"),           # Capitalización bursátil
                    # "dividendYield": info.get("dividendYield"),   # Rentabilidad por dividendo
                    # "payoutRatio": info.get("payoutRatio"),       # Ratio de pago de dividendos
                    # "currentRatio": info.get("currentRatio"),     # Ratio de liquidez corriente
                    # "quickRatio": info.get("quickRatio"),         # Ratio de liquidez inmediata
                    # "totalRevenue": info.get("totalRevenue"),     # Ingresos totales
                    # "grossMargins": info.get("grossMargins"),     # Margen bruto
                    # "operatingMargins": info.get("operatingMargins"), # Margen operativo
                    # "profitMargins": info.get("profitMargins"),   # Margen de beneficio neto
                    # "beta": info.get("beta"),                     # Volatilidad respecto al mercado
                    # "earningsGrowth": info.get("earningsGrowth"), # Crecimiento de beneficios
                    # "revenueGrowth": info.get("revenueGrowth"),   # Crecimiento de ingresos
                    # "country": info.get("country"),               # País de la empresa
                    # "website": info.get("website"),               # Web oficial de la empresa
                }
            except Exception as e:
                result = {
                    "nombre": nombre,
                    "ticker": ticker,
                    "error": str(e),
                    "comentario": f"No se pudo extraer información fundamental para {nombre} ({ticker})."
                }
            results.append(result)
        return results



# Helper para el grafo
def fundamental_node(state: ReportState) -> ReportState:
    node = FundamentalNode()
    return node(state)