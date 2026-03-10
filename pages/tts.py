import streamlit as st
from utils import APIClient
import io

# TTS Models configuration
TTS_MODELS = [
    {"name": "XTTS", "request_url": "https://gonna-assurance-kim-col.trycloudflare.com/v1/audio/speech"},
    {"name": "TTS Model v2", "request_url": "http://localhost:8002/tts/infer"},
    {"name": "TTS Model v3", "request_url": "http://localhost:8003/tts/infer"},
    {"name": "TTS Model v4", "request_url": "http://localhost:8004/tts/infer"},
]


def show():
    """Render TTS page"""
    st.title("🔊 Text-to-Speech (TTS)")
    st.markdown("Generate speech from text using your finetuned models")
    
    # Initialize session state
    if 'tts_generations' not in st.session_state:
        st.session_state.tts_generations = []
    if 'tts_latencies' not in st.session_state:
        st.session_state.tts_latencies = []
    
    # Sidebar configuration
    st.sidebar.markdown("### TTS Configuration")
    
    selected_model = st.sidebar.selectbox(
        "Select TTS Model:",
        options=range(len(TTS_MODELS)),
        format_func=lambda x: TTS_MODELS[x]["name"]
    )
    
    model_info = TTS_MODELS[selected_model]
    st.sidebar.code(model_info["request_url"], language="text")
    
    # Voice settings (optional)
    st.sidebar.markdown("#### Voice Settings")
    voice_speed = st.sidebar.slider("Speed", 0.5, 2.0, 1.0, 0.1)
    voice_pitch = st.sidebar.slider("Pitch", 0.5, 2.0, 1.0, 0.1)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Text Input")
        
        text_input = st.text_area(
            "Enter text to synthesize:",
            placeholder="Type the text you want to convert to speech...",
            height=200,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        generate_button = st.button(
            "🎵 Generate Audio",
            use_container_width=True,
            key="tts_generate"
        )
        
        if generate_button:
            if not text_input.strip():
                st.error("Please enter some text!")
            else:
                with st.spinner("Generating audio..."):
                    # Call TTS API
                    audio_bytes, latency = APIClient.tts_inference(
                        text_input,
                        model_info["request_url"]
                    )
                    
                    if audio_bytes:
                        # Store generation
                        st.session_state.tts_generations.append({
                            "text": text_input,
                            "model": model_info["name"],
                            "latency": latency,
                            "audio": audio_bytes
                        })
                        st.session_state.tts_latencies.append(latency)
                        st.success("✅ Audio generated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to generate audio. Please check the API connection.")
    
    with col2:
        st.subheader("Audio Output & Metrics")
        
        # Display latest generation
        if st.session_state.tts_generations:
            latest = st.session_state.tts_generations[-1]
            
            st.write("**Latest Generation:**")
            st.audio(latest["audio"], format="audio/wav")
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.metric(
                    "Latency",
                    f"{latest['latency']:.2f} ms",
                    help="Generation time"
                )
            
            with col_info2:
                st.metric(
                    "Model",
                    latest["model"],
                    help="Used model"
                )
            
            st.markdown("---")
            st.write(f"**Text:** {latest['text']}")
            
            # Display metrics
            if len(st.session_state.tts_latencies) > 1:
                st.subheader("Generation Metrics")
                import numpy as np
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    avg_latency = np.mean(st.session_state.tts_latencies)
                    st.metric("Avg Latency", f"{avg_latency:.2f} ms")
                
                with col_m2:
                    min_latency = np.min(st.session_state.tts_latencies)
                    st.metric("Min Latency", f"{min_latency:.2f} ms")
                
                with col_m3:
                    max_latency = np.max(st.session_state.tts_latencies)
                    st.metric("Max Latency", f"{max_latency:.2f} ms")
                
                st.line_chart(
                    {"Latency (ms)": st.session_state.tts_latencies},
                    use_container_width=True
                )
        else:
            st.info("📊 No audio generated yet. Start by entering text and clicking 'Generate Audio'!")
    
    # Generation history
    st.markdown("---")
    st.subheader("📜 Generation History")
    
    if st.session_state.tts_generations:
        # Display all generations
        for i, gen in enumerate(reversed(st.session_state.tts_generations), 1):
            idx = len(st.session_state.tts_generations) - i
            with st.expander(
                f"Generation #{i} - {gen['model']} ({gen['latency']:.2f}ms)",
                expanded=False
            ):
                col_h1, col_h2 = st.columns([2, 1])
                
                with col_h1:
                    st.write(f"**Text:** {gen['text']}")
                
                with col_h2:
                    st.caption(f"⏱️ {gen['latency']:.2f}ms")
                
                st.audio(gen["audio"], format="audio/wav")
        
        # Download button for latest
        if st.session_state.tts_generations:
            latest_audio = st.session_state.tts_generations[-1]["audio"]
            st.download_button(
                label="💾 Download Latest Audio",
                data=latest_audio,
                file_name="generated_audio.wav",
                mime="audio/wav",
                use_container_width=True
            )
        
        # Clear history
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.tts_generations = []
            st.session_state.tts_latencies = []
            st.rerun()
    else:
        st.info("No generations yet. Start by entering text!")


if __name__ == "__main__":
    show()
