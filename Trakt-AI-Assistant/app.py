import streamlit as st

from database import create_tables

st.set_page_config(
    page_title="Trakt AI Assistant",
    page_icon="🎬",
    layout="wide"
)

create_tables()

st.title("🎬 Trakt AI Assistant")

st.markdown("""
Welcome to your personal media intelligence system.

Use the sidebar to:

- 📊 Analyze your viewing habits
- 🎯 Get personalized recommendations
- 🤖 Chat with your AI assistant
- 🧠 Explore your taste profile
""")