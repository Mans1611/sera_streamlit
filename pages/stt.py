import streamlit as st
import time
import numpy as np
from utils import APIClient, MetricsCalculator
import soundfile as sf
import io

# STT Models configuration
STT_MODELS = [
    {"name": "wHISPER", "request_url": "https://cba4-2a02-ce0-1802-a53-2e58-b9ff-fe16-5bf7.ngrok-free.app/v1/audio/transcriptions"},
    {"name": "STT Model v2", "request_url": "http://localhost:8002/stt/infer"},
    {"name": "STT Model v3", "request_url": "http://localhost:8003/stt/infer"},
]


def show():
    """Render STT page"""
    st.title("🎤 Speech-to-Text (STT)")
    st.markdown("Convert speech to text using your finetuned models")
    
    # Initialize session state
    if 'stt_latencies' not in st.session_state:
        st.session_state.stt_latencies = []
    if 'stt_request_count' not in st.session_state:
        st.session_state.stt_request_count = 0
    if 'stt_transcriptions' not in st.session_state:
        st.session_state.stt_transcriptions = []
    
    # Sidebar configuration
    st.sidebar.markdown("### STT Configuration")
    
    selected_model = st.sidebar.selectbox(
        "Select STT Model:",
        options=range(len(STT_MODELS)),
        format_func=lambda x: STT_MODELS[x]["name"]
    )
    
    model_info = STT_MODELS[selected_model]
    st.sidebar.code(model_info["request_url"], language="text")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Options")
        
        input_type = st.radio(
            "Choose input method:",
            ["🎤 Record from Microphone", "📁 Upload Audio File"],
            label_visibility="collapsed"
        )
        
        audio_data = None
        sample_rate = None
        
        if input_type == "🎤 Record from Microphone":
            st.write("Click the button below to record audio from your microphone:")
            audio_data = st.audio_input("Record audio", label_visibility="collapsed")
            
        else:  # Upload file
            uploaded_file = st.file_uploader(
                "Upload an audio file (WAV, MP3, OGG)",
                type=["wav", "mp3", "ogg"]
            )
            if uploaded_file:
                audio_data = uploaded_file.read()
        
        # Process button
        if st.button("🚀 Transcribe", key="stt_process", use_container_width=True):
            if audio_data is None:
                st.error("Please provide audio input first!")
            else:
                with st.spinner("Processing audio..."):
                    # Call API
                    result, latency = APIClient.stt_inference(
                        audio_data,
                        model_info["request_url"]
                    )
                    
                    # Update metrics
                    st.session_state.stt_latencies.append(latency)
                    st.session_state.stt_request_count += 1
                    
                    # Store transcription
                    if "error" not in result:
                        transcription = result.get("text", result.get("transcription", ""))
                        st.session_state.stt_transcriptions.append({
                            "model": model_info["name"],
                            "text": transcription,
                            "latency": latency
                        })
                        st.success("✅ Transcription completed!")
                        st.write(f"**Transcription:** {transcription}")
                    else:
                        st.error(f"Error: {result['error']}")
    
    with col2:
        st.subheader("Metrics & Results")
        
        # Display metrics
        if st.session_state.stt_latencies:
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                avg_latency = MetricsCalculator.calculate_avg_latency(
                    st.session_state.stt_latencies
                )
                st.metric(
                    "Avg Latency",
                    f"{avg_latency:.2f} ms",
                    help="Average response time"
                )
                
                p95_latency = MetricsCalculator.calculate_p95_latency(
                    st.session_state.stt_latencies
                )
                st.metric(
                    "P95 Latency",
                    f"{p95_latency:.2f} ms",
                    help="95th percentile latency"
                )
            
            with col_m2:
                throughput = MetricsCalculator.calculate_throughput(
                    st.session_state.stt_request_count,
                    sum(st.session_state.stt_latencies)
                )
                st.metric(
                    "Throughput",
                    f"{throughput:.2f} req/s",
                    help="Requests per second"
                )
                
                st.metric(
                    "Total Requests",
                    st.session_state.stt_request_count,
                    help="Number of processed requests"
                )
            
            # Display chart
            st.line_chart(
                {
                    "Latency (ms)": st.session_state.stt_latencies
                },
                use_container_width=True
            )
        else:
            st.info("📊 Metrics will appear after your first transcription")
    
    # Transcription history
    st.markdown("---")
    st.subheader("📝 Transcription History")
    
    if st.session_state.stt_transcriptions:
        for i, trans in enumerate(reversed(st.session_state.stt_transcriptions), 1):
            with st.expander(f"Transcription #{len(st.session_state.stt_transcriptions) - i + 1} - {trans['model']}"):
                st.write(f"**Text:** {trans['text']}")
                st.write(f"**Latency:** {trans['latency']:.2f} ms")
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.stt_transcriptions = []
            st.session_state.stt_latencies = []
            st.session_state.stt_request_count = 0
            st.rerun()
    else:
        st.info("No transcriptions yet. Start by recording or uploading audio!")


if __name__ == "__main__":
    show()
