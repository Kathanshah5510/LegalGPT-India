import streamlit as st
import os
from src.chatbot import LegalChatbot

st.set_page_config(page_title="LegalGPT-India", page_icon="⚖️")

st.title("⚖️ LegalGPT-India")
st.markdown("### Your AI Assistant for the Constitution of India")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.info("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        if "chatbot" in st.session_state:
            # Re-initialize chatbot to clear its internal memory
            st.session_state.chatbot = LegalChatbot(api_key)
        st.rerun()

# Initialize Chatbot
if "chatbot" not in st.session_state and api_key:
    try:
        st.session_state.chatbot = LegalChatbot(api_key)
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")

# Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about the Constitution of India..."):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response, sources = st.session_state.chatbot.get_response(prompt)
                    st.markdown(response)
                    
                    # Display sources in an expander
                    if sources:
                        with st.expander("View Retrieved Articles"):
                            for i, src in enumerate(sources):
                                st.write(f"**Source {i+1} (Match: {src['score']:.2f})**")
                                st.text(src['article'][:1000] + "..." if len(src['article']) > 1000 else src['article'])
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
