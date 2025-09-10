# ia_client.py
"""
Módulo para gestionar la conexión y procesamiento de mensajes con la IA.
"""

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
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
    MediumModel = "gemini-2.5-flash" 
    SmallModel = "gpt-4o-mini"
    Alternative1 = "gemini-2.0-flash" 
    Alternative2 = ""
    Default = ""

MAX_TOKENS = 4092  # Máximo de tokens para las respuestas
IA_MODEL = IAModel.MediumModel  # Modelo por defecto
IA_EMBEDDINGS_MODEL = "azure"  # Modelo de embeddings por defecto: "azure" o "google"

class IAClient:
    # Perfiles de configuración para la IA
    PROFILES = {
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

    def __init__(self, config=None, profile = IAProfilesEnum.ANALYST, ia_model = None):
        """
        Inicializa el cliente de IA con Azure OpenAI y LangChain.
        Permite seleccionar un perfil de parámetros.
        """
        self.config = config or {}
        self.perfil = profile.value
        self.ia_model = ia_model

        # Inicializa el modelo de generación y embeddings
        self.llm = self._select_model(self.ia_model) # Modelo de texto
        self.embedding_model = self._init_embeddings() # Modelo de embeddings semánticos
        self.memory = ConversationBufferMemory()

    def _init_llm_text(self, ia_model = IAModel.SmallModel):
        """
        Inicializa el modelo LLM con los parámetros del perfil actual.
        """
        params = self.PROFILES.get(self.perfil, self.PROFILES["neutral"])
        if ia_model == IAModel.BigModel:         
            llm = AzureChatOpenAI(
                api_key=get_env_variable("AZURE_OPENAI_API_KEY", ""),
                azure_endpoint=get_env_variable("AZURE_OPENAI_ENDPOINT", ""),
                azure_deployment="gpt-4o-GM",
                api_version="2025-01-01-preview",
                temperature=params["temperature"],
                top_p=params["top_p"],
                max_tokens=params["max_tokens"]
            )
        if ia_model == IAModel.MediumModel:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=get_env_variable("GOOGLE_GEMINI_API_KEY"),
                temperature=params["temperature"],
                topP=params["top_p"],
                max_output_tokens=params["max_tokens"]
            )
        elif ia_model == IAModel.SmallModel:
            llm = AzureChatOpenAI(
                api_key=get_env_variable("AZURE_OPENAI_API_KEY", ""),
                azure_endpoint=get_env_variable("AZURE_OPENAI_ENDPOINT", ""),
                azure_deployment="gpt-4o-mini-GM",            
                api_version="2025-01-01-preview",
                temperature=params["temperature"],
                top_p=params["top_p"],
                max_tokens=params["max_tokens"]
            )
        elif ia_model == IAModel.Alternative1:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=get_env_variable("GOOGLE_GEMINI_API_KEY"), 
                temperature=params["temperature"],
                topP=params["top_p"],
                max_output_tokens=params["max_tokens"]
            )
            
        return llm
            

    def _init_embeddings(self, task_type="retrieval_query"):
        """
        Inicializa el modelo de embeddings usando AzureOpenAIEmbeddings.
        """
        if IA_EMBEDDINGS_MODEL == "azure":            
            embedding_model = AzureOpenAIEmbeddings(
                api_key=get_env_variable("AZURE_OPENAI_EMBEDDINGS_API_KEY"),
                azure_endpoint=get_env_variable("AZURE_OPENAI_EMBEDDINGS_ENDPOINT"),
                azure_deployment="text-embedding-ada-002",
                api_version="2023-05-15"
            )
        else:
            embedding_model = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=get_env_variable("GOOGLE_GEMINI_API_KEY"), # api key gratuita
                task_type=task_type  # o "retrieval_document", "classification", "clustering"
            )
        return embedding_model
        
    def _select_model(self, model: IAModel):
        """
        Selecciona el modelo de IA a usar.
        Si model es diferente de None es porque hemos llamado a la IA especificando un model concreto.
        Si model es None, se selecciona el modelo en función del modelo preestablecido en IA_MODEL;
        si IA_MODEL es Default, se selecciona el modelo en función del consumption_mode.
        """
        if model != None and model != IAModel.Default:
            llm = self._init_llm_text(model)
        else:
            defined_model = IA_MODEL
            if defined_model != IAModel.Default:
                llm = self._init_llm_text(defined_model)
                
        return llm


    def IA_call_process_message(self, message: str, context: str = None) -> str:
        """
        Procesa un mensaje usando la IA de Azure OpenAI y devuelve la respuesta generada.
        Si use_history=True, añade el historial de la conversación al contexto.
        """
        messages = []
        if context:
            messages.append(SystemMessage(content=context))
        messages.append(HumanMessage(content=message))
        response = self.llm.invoke(messages)
        return response.content
