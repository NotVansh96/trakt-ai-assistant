import streamlit as st

from database import create_tables

from auto_sync import auto_sync

st.set_page_config(
    page_title="Trakt AI Assistant",
    page_icon="🎬",
    layout="wide"
)

if "initial_sync" not in st.session_state:

    with st.spinner(
        "Syncing with Trakt..."
    ):

        auto_sync()

    st.session_state["initial_sync"] = True

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