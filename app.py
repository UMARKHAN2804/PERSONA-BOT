import streamlit as st
from langchain_groq import ChatGroq
st.set_page_config(page_title="Persona Bot")
st.title("🎭 The Persona Chatbot")
with st.sidebar:
    user_api_key = st.text_input("Groq API Key:", type="password")
    persona = st.text_area("Define the AI Persona:", value="You are a sarcastic robot.")
    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
if user_query := st.chat_input("Message the AI..."):
    if not user_api_key:
        st.error("Missing API Key.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        llm = ChatGroq(temperature=0.8, model_name="llama-3.3-70b-versatile", api_key=user_api_key)
        with st.spinner("AI is thinking..."):
            messages_for_llm = [{"role": "system", "content": persona}] + st.session_state.messages
            response = llm.invoke(messages_for_llm)
            bot_answer = response.content
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})
        with st.chat_message("assistant"):
            st.markdown(bot_answer)
