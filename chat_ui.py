import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000/chat"

# Initialize session state for chat history and session id
st.session_state.setdefault("messages", [])
st.session_state.setdefault("session_id", None)

# Streamlit UI
st.title("🤖 AI Chatbot")
st.write("Chat with your AI assistant. Messages persist in this session.")

# Display previous messages in order
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare the request payload with session id
    payload = {"message": user_input}
    if st.session_state.session_id is not None:
        payload["session_id"] = st.session_state.session_id

    # Send request to chatbot API
    response = requests.post(API_URL, json=payload)

    # Process the chatbot's response
    if response.status_code == 200:
        result = response.json()
        bot_response = result["response"]
        st.session_state.session_id = result["session_id"]
    else:
        bot_response = f"❌ Error {response.status_code}: {response.text}"

    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
