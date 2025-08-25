# ia_client.py
"""
Módulo para gestionar la conexión y procesamiento de mensajes con la IA.
"""

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from utils.env_loader import get_env_variable
from enum import Enum
from typing import List
from langchain.memory import ConversationBufferMemory

class IAProfilesEnum(str,Enum):
    CREATIVE = "creativa"
    PRECISE = "precisa"
    NEUTRAL = "neutral"
    RESUME = "resumen"
    CLASIFICATION = "clasificacion"
    ANALYST = "analista"  # Nuevo perfil analista

class IAModel(str, Enum):
    """
    Enum para definir los modelos de IA disponibles.
    """
    BigModel = "gpt-4o" 
    SmallModel = "gpt-4o-mini"
    Default = ""

MAX_TOKENS = 4092  # Máximo de tokens para las respuestas
IA_MODEL = IAModel.BigModel  # Modelo por defecto

class IAClient:
    # Perfiles de configuración para la IA
    PERFILES = {
        "creativa": {
            "temperature": 1.0,
            "top_p": 0.95,
            "max_tokens": MAX_TOKENS
        },
        "precisa": {
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": MAX_TOKENS
        },
        "neutral": {
            "temperature": 0.7,
            "top_p": 0.85,
            "max_tokens": MAX_TOKENS
        },
        "resumen": {
            "temperature": 0.3,
            "top_p": 0.8,
            "max_tokens": MAX_TOKENS
        },
        "clasificacion": {
            "temperature": 0.1,
            "top_p": 0.6,
            "max_tokens": MAX_TOKENS
        },
        "analista": { 
            "temperature": 0.5,
            "top_p": 0.9,
            "max_tokens": MAX_TOKENS
        }
    }   

    def __init__(self, config=None, perfil = IAProfilesEnum.ANALYST):
        """
        Inicializa el cliente de IA con Azure OpenAI y LangChain.
        Permite seleccionar un perfil de parámetros.
        """
        self.config = config or {}
        self.perfil = perfil.value
        self.ia_model = IAModel.Default

        # Inicializa el modelo de generación y embeddings
        self.llm = self._init_llm_text(IA_MODEL) # Modelo de texto
        # Inicializa la memoria de conversación
        self.memory = ConversationBufferMemory()

    def _init_llm_text(self, ia_model = IAModel.SmallModel):
        """
        Inicializa el modelo LLM con los parámetros del perfil actual.
        """
        params = self.PERFILES.get(self.perfil, self.PERFILES["neutral"])
        if ia_model == IAModel.BigModel:         
            llm = AzureChatOpenAI(
                azure_deployment=get_env_variable("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
                azure_endpoint=get_env_variable("AZURE_OPENAI_ENDPOINT", ""),
                api_version=get_env_variable("AZURE_OPENAI_API_VERSION", ""),
                api_key=get_env_variable("AZURE_OPENAI_API_KEY", ""),
                temperature=params["temperature"],
                top_p=params["top_p"],
                max_tokens=params["max_tokens"]
            )
        else:
            llm = AzureChatOpenAI(
                azure_deployment=get_env_variable("AZURE_OPENAI_DEPLOYMENT_NAME_SMALL", "gpt-4o-mini"),
                azure_endpoint=get_env_variable("AZURE_OPENAI_ENDPOINT_SMALL", ""),
                api_version=get_env_variable("AZURE_OPENAI_API_VERSION_SMALL", ""),
                api_key=get_env_variable("AZURE_OPENAI_API_KEY_SMALL", ""),
                temperature=params["temperature"],
                top_p=params["top_p"],
                max_tokens=params["max_tokens"]
            )
            
        return llm
            

    def IA_call_process_message(self, message: str, context: str = None, use_history: bool = False) -> str:
        """
        Procesa un mensaje usando la IA de Azure OpenAI y devuelve la respuesta generada.
        Si use_history=True, añade el historial de la conversación al contexto.
        """
        messages = []
        # Enriquecer el contexto con el historial si se solicita
        if use_history:
            history = self.get_history()
            if context:
                context = f"{context}\n\nHistorial:\n{history}"
            else:
                context = f"Historial:\n{history}"
        if context:
            messages.append(SystemMessage(content=context))
        messages.append(HumanMessage(content=message))
        response = self.llm.invoke(messages)
        self.add_message(message, response.content)
        return response.content


    def add_message(self, user_message: str, ai_message: str):
        """Agrega mensajes al historial de memoria."""
        self.memory.save_context({"input": user_message}, {"output": ai_message})

    def get_history(self) -> str:
        """Devuelve el historial completo de la conversación."""
        return self.memory.buffer
