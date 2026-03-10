# 🤖 AI Models Interface - Streamlit Application

A multi-page Streamlit application for testing and benchmarking your finetuned AI models (STT, LLM, TTS) via APIs.

## 📋 Features

### 🎤 Speech-to-Text (STT) Page
- **Input Methods:**
  - 🎤 Record directly from microphone
  - 📁 Upload audio files (WAV, MP3, OGG)
- **Model Selection:** Choose from multiple STT models
- **Metrics Tracking:**
  - Average latency
  - P95 latency
  - Throughput (requests/second)
  - Total requests processed
- **Transcription History:** View all past transcriptions with details

### 💬 LLM Chatbot Page
- **Interactive Chat:** Real-time chat interface with your models
- **Model Selection:** Switch between different LLM models
- **Auto-Reset:** Chat history automatically clears when switching models
- **Metrics:**
  - Average response time
  - Total messages and exchanges
- **Persistent History:** Chat messages saved per model

### 🔊 Text-to-Speech (TTS) Page
- **Text Input:** Enter text to synthesize
- **Voice Control:**
  - Speed adjustment (0.5x to 2.0x)
  - Pitch adjustment (0.5x to 2.0x)
- **Model Selection:** Choose from multiple TTS models
- **Audio Playback:** Play generated audio directly in the app
- **Download:** Download generated audio as WAV file
- **Metrics:**
  - Latency tracking
  - Min/Max/Average latency
  - Latency trends visualization
- **Generation History:** View all past generations

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Your finetuned models running as API endpoints

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

## ⚙️ Configuration

### Setting Up Model API Endpoints

You need to configure your models to run as API servers. Each model should have endpoints for inference.

Edit the model configurations in each page file:

**STT Models** - `pages/stt.py`:
```python
STT_MODELS = [
    {"name": "STT Model v1", "request_url": "http://localhost:8001/stt/infer"},
    {"name": "STT Model v2", "request_url": "http://localhost:8002/stt/infer"},
    # Add more models...
]
```

**LLM Models** - `pages/llm.py`:
```python
LLM_MODELS = [
    {"name": "LLM Model v1", "request_url": "http://localhost:8001/llm/infer"},
    {"name": "LLM Model v2", "request_url": "http://localhost:8002/llm/infer"},
    # Add more models...
]
```

**TTS Models** - `pages/tts.py`:
```python
TTS_MODELS = [
    {"name": "TTS Model v1", "request_url": "http://localhost:8001/tts/infer"},
    {"name": "TTS Model v2", "request_url": "http://localhost:8002/tts/infer"},
    # Add more models...
]
```

### API Endpoint Specifications

Your API endpoints should accept and return data in the following formats:

#### STT API Endpoint
**Request:**
```python
POST /stt/infer
Content-Type: multipart/form-data

Files:
- audio: wav/mp3/ogg audio file
```

**Response:**
```json
{
    "text": "transcribed text here",
    "confidence": 0.95
}
```

#### LLM API Endpoint
**Request:**
```python
POST /llm/infer
Content-Type: application/json

{
    "prompt": "user's text input"
}
```

**Response:**
```json
{
    "text": "model's response here"
}
```

or

```json
{
    "response": "model's response here"
}
```

#### TTS API Endpoint
**Request:**
```python
POST /tts/infer
Content-Type: application/json

{
    "text": "text to synthesize"
}
```

**Response:**
Returns binary audio file (WAV format)

## 📁 Project Structure

```
streamlit-app/
├── app.py                 # Main application entry point
├── utils.py               # API client and metrics calculator
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── pages/
    ├── stt.py            # Speech-to-Text page
    ├── llm.py            # LLM Chatbot page
    └── tts.py            # Text-to-Speech page
```

## 🔧 Utilities

### APIClient
Handles all API requests to your models:
- `stt_inference()` - Send audio and get transcription
- `llm_inference()` - Send text and get LLM response
- `tts_inference()` - Send text and get audio

### MetricsCalculator
Computes inference metrics:
- `calculate_throughput()` - Requests per second
- `calculate_avg_latency()` - Average response time
- `calculate_p95_latency()` - 95th percentile latency

## 📊 Monitoring & Metrics

The application automatically tracks:
- **Latency:** Response time for each request
- **Throughput:** Requests processed per second
- **Percentiles:** P95 latency for performance analysis
- **Trends:** Visual charts showing metric evolution

All metrics are displayed in real-time and updated as you use the models.

## 🎯 Tips

1. **STT:** Record short audio clips for faster processing
2. **LLM:** The chat resets when you change models - this is by design for clean conversations
3. **TTS:** Use varied text to test different aspects of your model
4. **Metrics:** Use latency data to identify performance bottlenecks
5. **Download:** Use the download button in TTS to save generated audio

## 🐛 Troubleshooting

**"API Connection Error"**
- Ensure your model API servers are running
- Check the request URLs in the configuration
- Verify network connectivity to the endpoints

**"Timeout Error"**
- Your model server might be slow
- Increase the timeout in `utils.py` (default: 30 seconds)
- Check server logs for errors

**"No Audio Recorded"**
- Grant microphone permissions to your browser
- Check browser console for errors
- Try uploading a file instead

## 📝 License

This project is open source and available for modification and distribution.

## 💡 Future Enhancements

- Add support for batch processing
- Export metrics to CSV/JSON
- Add speaker identification (STT)
- Add emotion detection (TTS)
- Real-time performance comparison between models
- Support for streaming responses (LLM)

---

Made with ❤️ using Streamlit
