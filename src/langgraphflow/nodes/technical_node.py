"""
Nodo/agente de análisis técnico para el grafo LangGraph.
"""
import os
import certifi
from src.langgraphflow.states.report_state import ReportState
from src.langgraphflow.states.report_state_manager import ReportStateManager
import yfinance as yf
import pandas as pd

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
                    "MA20": self._get_indicator('MA20', last),
                    "MA50": self._get_indicator('MA50', last),
                    "RSI": self._get_indicator('RSI', last),
                    "MACD": self._get_indicator('MACD', last),
                    "Signal": self._get_indicator('Signal', last),
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

    def _safe_float(self, val):
        if pd.isna(val):
            return None
        try:
            return float(val)
        except Exception:
            return str(val)
        
    def _get_indicator(self,ind, last):
        val = last.get(ind, None) if hasattr(last, 'get') else last[ind] if ind in last else None
        if val is None:
            return None
        try:
            return self._safe_float(round(val, 2))
        except Exception:
            return None

# Helper para el grafo
def technical_node(state: ReportState) -> ReportState:
    node = TechnicalNode()
    return node(state)