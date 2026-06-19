import streamlit as st

from gemini_ai import (
    generate_taste_profile
)

from database import (
    get_taste_profile
)

from style import load_css

st.set_page_config(
    page_title="Taste Profile",
    page_icon="🧠",
    layout="wide"
)

load_css()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 🧠 Taste Profile

Understand your entertainment DNA.
""")

# --------------------------------------------------
# Generate Profile
# --------------------------------------------------

if st.button(
    "Generate My Profile"
):

    with st.spinner(
        "Analyzing ratings..."
    ):

        generate_taste_profile()

    st.success(
        "Profile generated successfully."
    )

# --------------------------------------------------
# Load Profile
# --------------------------------------------------

profile = get_taste_profile()

if not profile:

    st.info(
        "Generate your taste profile to begin."
    )

    st.stop()

# --------------------------------------------------
# Display Profile
# --------------------------------------------------

sections = {}

current_section = None

for line in profile.splitlines():

    line = line.strip()

    if not line:
        continue

    if ":" in line:

        key, value = line.split(
            ":",
            1
        )

        current_section = key.strip()

        sections[current_section] = value.strip()

# --------------------------------------------------
# Layout
# --------------------------------------------------

col1, col2 = st.columns(2)

section_items = list(
    sections.items()
)

for i, (title, content) in enumerate(
    section_items
):

    current_col = (
        col1
        if i % 2 == 0
        else col2
    )

    with current_col:

        with st.container(border=True):

            st.subheader(
                title.title()
            )

            items = [
                item.strip()
                for item in content.split(",")
                if item.strip()
            ]

            for item in items:

                st.caption(
                    f"• {item}"
                )