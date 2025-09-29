# AIBrokerAssistance

AIBrokerAssistance es un proyecto diseñado para asistir en la gestión de brokers utilizando inteligencia artificial. Este README proporciona una visión general de la estructura del proyecto y sus componentes principales.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
AIBrokerAssistance/
├── .env                # Archivo de configuración de entorno
├── .git/               # Archivos de control de versiones
├── .gitignore          # Configuración para ignorar archivos en Git
├── .vscode/            # Configuración específica de VSCode
│   └── launch.json     # Configuración de lanzamiento para depuración
├── doc/                # Documentación del proyecto
│   └── AIBrokerAssistance.odt
├── main.py             # Archivo principal del proyecto
├── README.md           # Este archivo
├── requirements.txt    # Dependencias del proyecto
├── src/                # Código fuente principal
│   ├── chat_manager.py
│   ├── ia_client.py
│   └── langgraphflow/  # Módulo para gestión de grafos
│       ├── __init__.py
│       ├── graph_manager.py
│       ├── chains/     # Directorio vacío
│       ├── nodes/      # Implementación de nodos
│       │   ├── fundamental_node.py
│       │   ├── news_node.py
│       │   ├── orquestator_node.py
│       │   ├── synthesis_node.py
│       │   └── technical_node.py
│       ├── states/     # Gestión de estados
│       │   ├── report_state.py
│       │   └── report_state_manager.py
│       └── utils/      # Herramientas auxiliares
│           └── node_tool.py
├── utils/              # Utilidades generales
│   ├── env_loader.py
│   ├── notebooks/      # Notebooks para visualización
│   │   ├── graph.dot
│   │   ├── graph_output.png
│   │   └── visualize_graph.ipynb
│   └── utils.py
└── venv/               # Entorno virtual de Python
```

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/FranciscoJRobles/AIBrokerAssistance.git
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd AIBrokerAssistance
   ```

3. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   source venv/bin/activate  # En Unix/MacOS
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el archivo principal para iniciar el proyecto:
```bash
python main.py
```

## Contribución

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad o corrección de errores:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz commit:
   ```bash
   git commit -m "Añadida nueva funcionalidad"
   ```
4. Sube tus cambios a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un Pull Request en este repositorio.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
