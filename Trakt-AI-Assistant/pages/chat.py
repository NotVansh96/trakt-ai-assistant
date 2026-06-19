import streamlit as st

from gemini_ai import ask_gemini

from style import load_css

load_css()

st.title("🤖 AI Chat")

user_message = st.chat_input(
    "Ask me anything..."
)

if user_message:

    st.chat_message("user").write(
        user_message
    )

    with st.spinner("Thinking..."):
        answer = ask_gemini(user_message)

    st.chat_message("assistant").write(
        answer
    )