# Model Configuration
# Edit this file to configure your model API endpoints

MODELS_CONFIG = {
    "stt": [
        {"name": "STT Model v1", "request_url": "http://localhost:8001/stt/infer"},
        {"name": "STT Model v2", "request_url": "http://localhost:8002/stt/infer"},
        {"name": "STT Model v3", "request_url": "http://localhost:8003/stt/infer"},
    ],
    "llm": [
        {"name": "LLM Model v1", "request_url": "http://localhost:8001/llm/infer"},
        {"name": "LLM Model v2", "request_url": "http://localhost:8002/llm/infer"},
        {"name": "LLM Model v3", "request_url": "http://localhost:8003/llm/infer"},
        {"name": "LLM Model v4", "request_url": "http://localhost:8004/llm/infer"},
    ],
    "tts": [
        {"name": "TTS Model v1", "request_url": "http://localhost:8001/tts/infer"},
        {"name": "TTS Model v2", "request_url": "http://localhost:8002/tts/infer"},
        {"name": "TTS Model v3", "request_url": "http://localhost:8003/tts/infer"},
        {"name": "TTS Model v4", "request_url": "http://localhost:8004/tts/infer"},
    ]
}

# API Settings
API_TIMEOUT = 30  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds
