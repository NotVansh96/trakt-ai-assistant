import streamlit as st
from omdb_api import get_poster_by_title
import pandas as pd

from database import (
    get_database_stats,
    get_rating_distribution_by_type,
    get_most_watched_shows,
    get_watchtime_stats,
    get_last_30_days_watchtime,
    get_last_7_days_activity
)

from style import load_css

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

load_css()

stats = get_database_stats()

rating_distribution = get_rating_distribution_by_type()

most_watched = get_most_watched_shows()

watchtime = get_watchtime_stats()

last30 = get_last_30_days_watchtime()

activity = get_last_7_days_activity()

# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown("""
# 📊 Analytics

Understand your viewing habits, watch time,
and entertainment preferences.
""")

# --------------------------------------------------
# Watch Time
# --------------------------------------------------

st.header(
    "⏱ Watch Time",
    divider="blue"
)

total_hours = watchtime["total_minutes"] // 60
movie_hours = watchtime["movies_minutes"] // 60
episode_hours = watchtime["episodes_minutes"] // 60
last30_hours = last30 // 60

with st.container(border=True):

    st.markdown(
        f"""
# ⏱ {total_hours:,} Hours

Total Time Watched
"""
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🎬 Movies",
            f"{movie_hours:,}h"
        )

    with c2:
        st.metric(
            "📺 Episodes",
            f"{episode_hours:,}h"
        )

    with c3:
        st.metric(
            "📅 Last 30 Days",
            f"{last30_hours:,}h"
        )

# --------------------------------------------------
# Overview
# --------------------------------------------------

st.header(
    "📈 Overview",
    divider="red"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Watched",
        stats["total"]
    )

with c2:
    st.metric(
        "Movies",
        stats["movies"]
    )

with c3:
    st.metric(
        "Episodes",
        stats["episodes"]
    )

st.header(
    "🎭 Viewing Breakdown",
    divider="violet"
)

total = stats["total"]

movie_pct = round(
    (stats["movies"] / total) * 100,
    1
)

episode_pct = round(
    (stats["episodes"] / total) * 100,
    1
)

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Movies %",
        f"{movie_pct}%"
    )

with c2:
    st.metric(
        "Episodes %",
        f"{episode_pct}%"
    )

# --------------------------------------------------
# Rating Distribution
# --------------------------------------------------

st.header(
    "⭐ Rating Distribution",
    divider="orange"
)

ratings_df = pd.DataFrame(
    rating_distribution,
    columns=[
        "Rating",
        "Type",
        "Count"
    ]
)

pivot_df = ratings_df.pivot(
    index="Rating",
    columns="Type",
    values="Count"
).fillna(0)

pivot_df = pivot_df.rename(
    columns={
        "movie": "🎬 Movies",
        "show": "📺 Shows"
    }
)

highest_rating = ratings_df["Rating"].max()

st.caption(
    f"Distribution of your ratings across movies and shows."
)

st.bar_chart(
    pivot_df
)

# --------------------------------------------------
# Most Watched Shows
# --------------------------------------------------

st.header(
    "📺 Most Watched Shows",
    divider="green"
)

show_cols = st.columns(3)

medals = ["🥇", "🥈", "🥉"]

for i, (title, episodes) in enumerate(most_watched[:9]):

    with show_cols[i % 3]:

        with st.container(border=True):

            poster = get_poster_by_title(title)

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.image(
                    "https://placehold.co/300x450?text=No+Poster",
                    use_container_width=True
                )

            rank = f"#{i+1}"

            if i < 3:
                rank = medals[i]

            st.markdown(
                f"# {rank}"
            )

            st.markdown(
                f"### {title}"
            )

            st.metric(
                "Episodes", episodes
            )