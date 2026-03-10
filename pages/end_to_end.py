import streamlit as st
import time
from utils import APIClient, MetricsCalculator
import numpy as np

# Models configuration
STT_MODELS = [
    {"name": "wHISPER", "request_url": "https://cba4-2a02-ce0-1802-a53-2e58-b9ff-fe16-5bf7.ngrok-free.app/v1/audio/transcriptions"}
]

LLM_MODELS = [
    {"name": "OpenAI", "request_url": "https://hose-medal-designated-partnerships.trycloudflare.com/v1/messages"}
]

TTS_MODELS = [
    {"name": "XTTS", "request_url": "https://gonna-assurance-kim-col.trycloudflare.com/v1/audio/speech"}
]


def show():
    """Render integrated end-to-end voice assistant page"""
    st.set_page_config(page_title="Voice Assistant", layout="wide")
    
    # Custom CSS for modern styling
    st.markdown("""
    <style>
        .flow-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 20px 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
        }
        .flow-step {
            text-align: center;
            flex: 1;
        }
        .flow-arrow {
            font-size: 24px;
            margin: 0 10px;
        }
        .step-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .step-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .response-container {
            background: #f0f2f6;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .metrics-box {
            background: #e8f4f8;
            border-left: 4px solid #00d4ff;
            padding: 12px;
            border-radius: 5px;
            margin: 5px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'e2e_conversation_history' not in st.session_state:
        st.session_state.e2e_conversation_history = []
    if 'e2e_current_text' not in st.session_state:
        st.session_state.e2e_current_text = ""
    if 'e2e_current_response' not in st.session_state:
        st.session_state.e2e_current_response = ""
    if 'e2e_current_audio' not in st.session_state:
        st.session_state.e2e_current_audio = None
    
    # Title
    st.title("🎙️ Voice Assistant")
    st.markdown("**Speak → Understand → Respond**")
    
    # Flow visualization
    st.markdown("""
    <div class="flow-container">
        <div class="flow-step">
            <div class="step-icon">🎤</div>
            <div class="step-title">Record Voice</div>
            <div style="font-size: 12px;">Speech to Text</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">
            <div class="step-icon">🧠</div>
            <div class="step-title">Process</div>
            <div style="font-size: 12px;">Language Model</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">
            <div class="step-icon">🔊</div>
            <div class="step-title">Respond</div>
            <div style="font-size: 12px;">Text to Speech</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar - Model Selection
    st.sidebar.markdown("### ⚙️ Configuration")
    
    with st.sidebar.expander("🎤 STT Model", expanded=True):
        selected_stt = st.selectbox(
            "Select Speech-to-Text Model:",
            options=range(len(STT_MODELS)),
            format_func=lambda x: STT_MODELS[x]["name"],
            key="e2e_stt_model"
        )
        stt_model = STT_MODELS[selected_stt]
    
    with st.sidebar.expander("🧠 LLM Model", expanded=True):
        selected_llm = st.selectbox(
            "Select Language Model:",
            options=range(len(LLM_MODELS)),
            format_func=lambda x: LLM_MODELS[x]["name"],
            key="e2e_llm_model"
        )
        llm_model = LLM_MODELS[selected_llm]
    
    with st.sidebar.expander("🔊 TTS Model", expanded=True):
        selected_tts = st.selectbox(
            "Select Text-to-Speech Model:",
            options=range(len(TTS_MODELS)),
            format_func=lambda x: TTS_MODELS[x]["name"],
            key="e2e_tts_model"
        )
        tts_model = TTS_MODELS[selected_tts]
    
    # Main content - Step 1: Record Audio
    st.markdown("### Step 1️⃣: Record Your Voice")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Choose input method:**")
        input_type = st.radio(
            "Input method:",
            ["🎤 Record from Microphone", "📁 Upload Audio File"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    audio_data = None
    
    if input_type == "🎤 Record from Microphone":
        audio_data = st.audio_input("Record your voice:", label_visibility="collapsed")
    else:
        uploaded_file = st.file_uploader(
            "Upload audio file:",
            type=["wav", "mp3", "ogg"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            audio_data = uploaded_file.read()
    
    # Process button
    process_button = st.button(
        "🚀 Process Voice Request",
        use_container_width=True,
        type="primary"
    )
    
    if process_button:
        if audio_data is None:
            st.error("❌ Please provide audio input first!")
        else:
            # Container for the entire process
            process_container = st.container()
            
            with process_container:
                # Step 1: STT
                with st.spinner("🎤 Converting speech to text..."):
                    stt_start = time.time()
                    stt_result, stt_latency = APIClient.stt_inference(
                        audio_data,
                        stt_model["request_url"]
                    )
                    stt_time = time.time() - stt_start
                    
                    if "error" in stt_result:
                        st.error(f"❌ STT Error: {stt_result['error']}")
                        st.stop()
                    
                    transcribed_text = stt_result.get("text", stt_result.get("transcription", ""))
                    st.session_state.e2e_current_text = transcribed_text
                
                # Display transcribed text
                st.markdown("### Step 2️⃣: Your Message")
                st.markdown(f'<div class="response-container"><b>You:</b> "{transcribed_text}"</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="metrics-box"><b>⏱️ Speech Recognition Time:</b> {stt_latency:.2f}ms</div>', unsafe_allow_html=True)
                
                # Step 2: LLM
                with st.spinner("🧠 Processing with AI..."):
                    llm_start = time.time()
                    llm_response, llm_latency = APIClient.llm_inference(
                        transcribed_text,
                        llm_model["request_url"]
                    )
                    llm_time = time.time() - llm_start
                    
                    st.session_state.e2e_current_response = llm_response
                
                # Display LLM response
                st.markdown("### Step 3️⃣: AI Response")
                st.markdown(f'<div class="response-container"><b>Assistant:</b> "{llm_response}"</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="metrics-box"><b>⏱️ AI Processing Time:</b> {llm_latency:.2f}ms</div>', unsafe_allow_html=True)
                
                # Step 3: TTS
                with st.spinner("🔊 Generating speech response..."):
                    tts_start = time.time()
                    tts_audio, tts_latency = APIClient.tts_inference(
                        llm_response,
                        tts_model["request_url"]
                    )
                    tts_time = time.time() - tts_start
                    
                    if tts_audio is None:
                        st.warning("⚠️ TTS generation failed. But here's the text response:")
                    else:
                        st.session_state.e2e_current_audio = tts_audio
                
                # Display audio response
                st.markdown("### Step 4️⃣: Listen to Response")
                
                if st.session_state.e2e_current_audio:
                    st.audio(st.session_state.e2e_current_audio, format="audio/wav")
                    st.markdown(f'<div class="metrics-box"><b>⏱️ Speech Generation Time:</b> {tts_latency:.2f}ms</div>', unsafe_allow_html=True)
                else:
                    st.info("Audio generation unavailable. Text response shown above.")
                
                # Overall metrics
                st.markdown("---")
                st.markdown("### 📊 Performance Metrics")
                
                total_time = stt_time + llm_time + tts_time
                
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    st.metric(
                        "STT Time",
                        f"{stt_latency:.2f}ms",
                        help="Speech to text latency"
                    )
                
                with col_m2:
                    st.metric(
                        "LLM Time",
                        f"{llm_latency:.2f}ms",
                        help="Language model latency"
                    )
                
                with col_m3:
                    st.metric(
                        "TTS Time",
                        f"{tts_latency:.2f}ms",
                        help="Text to speech latency"
                    )
                
                with col_m4:
                    st.metric(
                        "Total Time",
                        f"{total_time:.2f}s",
                        help="Total processing time"
                    )
                
                # Save to history
                st.session_state.e2e_conversation_history.append({
                    "timestamp": time.time(),
                    "input": transcribed_text,
                    "response": llm_response,
                    "audio": tts_audio,
                    "stt_latency": stt_latency,
                    "llm_latency": llm_latency,
                    "tts_latency": tts_latency,
                    "models": {
                        "stt": stt_model["name"],
                        "llm": llm_model["name"],
                        "tts": tts_model["name"]
                    }
                })
                
                st.success("✅ Processing complete!")
    
    # Conversation history
    if st.session_state.e2e_conversation_history:
        st.markdown("---")
        st.markdown("### 📝 Conversation History")
        
        for i, conv in enumerate(reversed(st.session_state.e2e_conversation_history), 1):
            idx = len(st.session_state.e2e_conversation_history) - i
            
            with st.expander(
                f"Interaction #{i} - {conv['models']['stt']} → {conv['models']['llm']} → {conv['models']['tts']}",
                expanded=False
            ):
                col_h1, col_h2 = st.columns([2, 1])
                
                with col_h1:
                    st.markdown(f"**Your input:** {conv['input']}")
                    st.markdown(f"**AI response:** {conv['response']}")
                
                with col_h2:
                    st.metric("Total Latency", f"{conv['stt_latency'] + conv['llm_latency'] + conv['tts_latency']:.2f}ms")
                
                if conv['audio']:
                    st.audio(conv['audio'], format="audio/wav")
        
        # Clear history button
        col_clear1, col_clear2 = st.columns([3, 1])
        with col_clear2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.e2e_conversation_history = []
                st.rerun()


if __name__ == "__main__":
    show()
