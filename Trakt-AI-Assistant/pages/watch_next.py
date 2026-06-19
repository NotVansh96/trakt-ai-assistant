import re
import streamlit as st

from omdb_api import get_poster_by_title
from gemini_ai import rank_watchlist

from style import load_css

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Watch Next",
    page_icon="🎯",
    layout="wide"
)

load_css()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 🎯 Watch Next

Discover the best titles from your watchlist based on
your ratings, watch history and taste profile.
""")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Generate Recommendations
# --------------------------------------------------

if st.button(
    "🚀 Generate Recommendations",
    use_container_width=True
):

    with st.spinner(
        "Analyzing your watchlist..."
    ):

        recommendations = rank_watchlist()

    st.session_state["recommendations"] = recommendations

# --------------------------------------------------
# Parser
# --------------------------------------------------

def parse_recommendations(text):

    pattern = r"#(\d+)\s+(.*?)\n\nMatch Score:\s*(\d+)(.*?)(?=#\d+|\Z)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    recommendations = []

    for rank, title, score, content in matches:

        recommendations.append(
            {
                "rank": int(rank),
                "title": title.strip(),
                "score": int(score),
                "content": content.strip()
            }
        )

    return recommendations

# --------------------------------------------------
# Results
# --------------------------------------------------

if "recommendations" in st.session_state:

    parsed = parse_recommendations(
        st.session_state["recommendations"]
    )

    st.header(
        "🔥 Recommended For You",
        divider="orange"
    )

    if not parsed:

        st.warning(
            "No recommendations found."
        )

    for rec in parsed:

        with st.container(border=True):

            left, right = st.columns(
                [1.2, 2.8]
            )

            with left:

                poster = get_poster_by_title(
                    rec["title"]
                )

                if poster:

                    st.image(
                        poster,
                        width=280
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )

            with right:

                st.markdown(
                    f"## 🏆 #{rec['rank']}"
                )

                st.markdown(
                    f"# {rec['title']}"
                )

                st.progress(
                    rec["score"] / 100
                )

                st.caption(
                    f"{rec['score']}% Match"
                )

                st.markdown(
                    rec["content"]
                )

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )