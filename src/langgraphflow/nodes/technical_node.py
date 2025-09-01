"""
Nodo/agente de análisis técnico para el grafo LangGraph.
"""
import os
import certifi
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
import yfinance as yf
import pandas as pd

# Configuración de certificados (ajusta la ruta si usas symlink)
os.environ['SSL_CERT_FILE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
os.environ['REQUESTS_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"
os.environ['CURL_CA_BUNDLE'] = r"D:\certs\AIBrokerLink\venv\Lib\site-packages\certifi\cacert.pem"

print("Usando certificado en:", certifi.where())

class TechnicalNode:

    def __init__(self):
        pass

    def __call__(self, state: ReportState) -> ReportState:
        try:
            state_manager = ReportStateManager(state)
            companies = state_manager.get_companies()  # Lista de dicts con nombre y ticker

            resultado = self.get_technical_result(companies)
            state_manager.set_technical_result(resultado)
            return state
        except Exception as e:
            print(f"TechnicalNode: Error al ejecutar el nodo: {e}")
            state_manager.set_technical_result({"error": str(e)})
            return state

    def get_technical_result(self, companies) -> dict:
        """
        Recopila información técnica usando yfinance y pandas.
        Devuelve un dict con los indicadores relevantes por empresa.
        """
        results = []
        for company in companies:
            ticker = company.get("ticker")
            nombre = company.get("nombre")
            if not ticker:
                continue
            try:
                stock = yf.Ticker(ticker)
                # Descarga datos históricos (últimos 6 meses, puedes ajustar)
                df = stock.history(period="6mo", interval="1d")
                if df.empty:
                    raise Exception("No hay datos históricos disponibles.")

                # Indicadores técnicos
                df['MA20'] = df['Close'].rolling(window=20).mean()  # Media móvil 20 días
                df['MA50'] = df['Close'].rolling(window=50).mean()  # Media móvil 50 días

                # RSI (Relative Strength Index)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))

                # MACD
                exp12 = df['Close'].ewm(span=12, adjust=False).mean()
                exp26 = df['Close'].ewm(span=26, adjust=False).mean()
                df['MACD'] = exp12 - exp26
                df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

                # Últimos valores
                last = df.iloc[-1]
                result = {
                    "nombre": nombre,
                    "ticker": ticker,
                    "MA20": round(last['MA20'], 2) if not pd.isna(last['MA20']) else None,
                    "MA50": round(last['MA50'], 2) if not pd.isna(last['MA50']) else None,
                    "RSI": round(last['RSI'], 2) if not pd.isna(last['RSI']) else None,
                    "MACD": round(last['MACD'], 2) if not pd.isna(last['MACD']) else None,
                    "Signal": round(last['Signal'], 2) if not pd.isna(last['Signal']) else None,
                    "comentario": f"Indicadores técnicos de {nombre} ({ticker}) extraídos correctamente."
                }
            except Exception as e:
                result = {
                    "nombre": nombre,
                    "ticker": ticker,
                    "error": str(e),
                    "comentario": f"No se pudo extraer información técnica para {nombre} ({ticker})."
                }
            results.append(result)
        return results

# Helper para el grafo
def technical_node(state: ReportState) -> ReportState:
    node = TechnicalNode()
    return node(state)