import streamlit as st
from utils import APIClient
import time

# LLM Models configuration
LLM_MODELS = [
    {"name": "OpenAI", "request_url": "https://hose-medal-designated-partnerships.trycloudflare.com/v1/messages"},
    {"name": "LLM Model v2", "request_url": "http://localhost:8002/llm/infer"},
    {"name": "LLM Model v3", "request_url": "http://localhost:8003/llm/infer"},
    {"name": "LLM Model v4", "request_url": "http://localhost:8004/llm/infer"},
]


def show():
    """Render LLM Chatbot page"""
    st.title("💬 Large Language Model (LLM) Chatbot")
    st.markdown("Chat with your finetuned language models")
    
    # Initialize session state
    if 'llm_chat_history' not in st.session_state:
        st.session_state.llm_chat_history = {}
    if 'llm_selected_model' not in st.session_state:
        st.session_state.llm_selected_model = 0
    if 'llm_latencies' not in st.session_state:
        st.session_state.llm_latencies = []
    
    # Sidebar configuration
    st.sidebar.markdown("### LLM Configuration")
    
    # Model selection
    new_model_idx = st.sidebar.selectbox(
        "Select LLM Model:",
        options=range(len(LLM_MODELS)),
        format_func=lambda x: LLM_MODELS[x]["name"],
        key="llm_model_selector"
    )
    
    # Check if model changed - reset chat if so
    if new_model_idx != st.session_state.llm_selected_model:
        st.session_state.llm_selected_model = new_model_idx
        st.session_state.llm_chat_history = {}
        st.session_state.llm_latencies = []
        st.rerun()
    
    model_info = LLM_MODELS[st.session_state.llm_selected_model]
    st.sidebar.code(model_info["request_url"], language="text")
    
    # Initialize current model's chat history
    if st.session_state.llm_selected_model not in st.session_state.llm_chat_history:
        st.session_state.llm_chat_history[st.session_state.llm_selected_model] = []
    
    current_chat = st.session_state.llm_chat_history[st.session_state.llm_selected_model]
    
    # Display chat history
    st.subheader("Chat Messages")
    chat_container = st.container(border=True, height=400)
    
    with chat_container:
        if current_chat:
            for message in current_chat:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    if message["role"] == "assistant":
                        st.caption(f"⏱️ Latency: {message.get('latency', 0):.2f}ms")
        else:
            st.info("👋 Start a conversation by typing a message below!")
    
    # Input area
    st.markdown("---")
    
    col_input, col_send = st.columns([5, 1])
    
    with col_input:
        user_input = st.text_input(
            "Your message:",
            placeholder="Type something...",
            label_visibility="collapsed",
            key=f"llm_input_{st.session_state.llm_selected_model}"
        )
    
    with col_send:
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        send_button = st.button("Send", use_container_width=True, key="llm_send")
    
    # Process message
    if send_button and user_input.strip():
        # Add user message to chat
        current_chat.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response from API
        with st.spinner("Waiting for response..."):
            response_text, latency = APIClient.llm_inference(
                user_input,
                model_info["request_url"]
            )
            
            # Add assistant response to chat
            current_chat.append({
                "role": "assistant",
                "content": response_text,
                "latency": latency
            })
            
            st.session_state.llm_latencies.append(latency)
            st.rerun()
    
    # Sidebar stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Chat Statistics")
    
    if st.session_state.llm_latencies:
        import numpy as np
        avg_latency = np.mean(st.session_state.llm_latencies)
        st.sidebar.metric("Avg Response Time", f"{avg_latency:.2f}ms")
        st.sidebar.metric("Total Messages", len(current_chat))
        st.sidebar.metric("Total Exchanges", len(current_chat) // 2)
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.llm_chat_history[st.session_state.llm_selected_model] = []
        st.session_state.llm_latencies = []
        st.rerun()


if __name__ == "__main__":
    show()
