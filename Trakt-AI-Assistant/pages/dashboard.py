import streamlit as st

from omdb_api import (
    get_poster,
    get_poster_by_title
)

from trakt_api import (
    get_profile,
    get_user_stats
)

from database import (
    get_recent_movies,
    get_recent_episodes,
    get_top_rated,
    get_watchlist_count
)

from gemini_ai import (
    get_top_recommendations
)

from style import load_css

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Vansh's Watch Party",
    page_icon="🎬",
    layout="wide"
)

load_css()

st.markdown("""
<style>

/* Reduce top padding */
.block-container {
    padding-top: 2rem;
}

/* Card hover effect */
[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
    transition: all 0.2s ease;
}

[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
}

/* Cleaner metrics */
[data-testid="metric-container"] {
    border-radius: 12px;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

profile = get_profile()

if not profile:
    st.error("Unable to load Trakt profile.")
    st.stop()

stats = get_user_stats()

recent_movies = get_recent_movies()
recent_episodes = get_recent_episodes()

top_rated = get_top_rated(5)

watchlist_count = get_watchlist_count()

recommendations = get_top_recommendations()


user = profile["user"]

# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown(
    f"""
# 🎬 Vansh's Watch Party

### Welcome back, {user['username']}

Your personal entertainment intelligence platform.

Track what you watch • Understand your taste • Discover what to watch next
"""
)

st.caption(
    f"""
🎬 {stats['movies']['watched']} Movies •
📺 {stats['episodes']['watched']} Episodes •
⭐ {stats['ratings']['total']} Ratings •
📚 {watchlist_count} Watchlist Items
"""
)

hero1, hero2, hero3, hero4 = st.columns(4)

with hero1:
    with st.container(border=True):
        st.metric(
            "🎬 Movies",
            stats["movies"]["watched"]
        )

with hero2:
    with st.container(border=True):
        st.metric(
            "📺 Episodes",
            stats["episodes"]["watched"]
        )

with hero3:
    with st.container(border=True):
        st.metric(
            "⭐ Ratings",
            stats["ratings"]["total"]
        )

with hero4:
    with st.container(border=True):
        st.metric(
            "📚 Watchlist",
            watchlist_count
        )

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Recently Watched Movies
# --------------------------------------------------

st.header(
    "🎬 Recently Watched Movies",
    divider="orange"
)

movie_cols = st.columns(5)

for i, (title, watched_at, imdb_id) in enumerate(recent_movies[:5]):

    with movie_cols[i]:

        poster = get_poster(imdb_id)

        if poster:
            st.image(
                poster,
                use_container_width=True
            )

        st.markdown(
            f"**{title}**"
        )

# --------------------------------------------------
# Recently Watched Episodes
# --------------------------------------------------

st.header(
    "📺 Recently Watched Episodes",
    divider="orange"
)

episode_cols = st.columns(5)

for i, (title, season, episode, episode_title) in enumerate(
    recent_episodes[:5]
):

    with episode_cols[i]:

        poster = get_poster_by_title(title)

        if poster:
            st.image(
                poster,
                use_container_width=True
            )

        st.markdown(
            f"**{title}**"
        )

        st.caption(
            f"S{season:02d}E{episode:02d}"
        )

        st.caption(
            episode_title
        )

# --------------------------------------------------
# Recommended For You
# --------------------------------------------------

st.header(
    "🎯 Recommended For You",
    divider="violet"
)

st.caption(
    "Personalized picks based on your ratings and watch history"
)

recommendation_cols = st.columns(
    len(recommendations)
)

for i, title in enumerate(recommendations):

    with recommendation_cols[i]:

        poster = get_poster_by_title(title)

        if poster:
            st.image(
                poster,
                width=180
            )

        st.caption(title)

# --------------------------------------------------
# Your Favorites
# --------------------------------------------------

st.header(
    "⭐ Your Favorites",
    divider="green"
)

favorite_items = top_rated[:5]

favorite_cols = st.columns(
    len(favorite_items)
)

for i, (title, rating) in enumerate(favorite_items):

    with favorite_cols[i]:

        poster = get_poster_by_title(title)

        if poster:
            st.image(
                poster,
                width=180
            )

        st.caption(title)

        st.caption(
            f"⭐ {rating}/10"
        )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    f"""
🎬 {stats['movies']['watched']} Movies •
📺 {stats['episodes']['watched']} Episodes •
⭐ {stats['ratings']['total']} Ratings •
📚 {watchlist_count} Watchlist Items
"""
)