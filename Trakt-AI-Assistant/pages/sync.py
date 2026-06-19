import streamlit as st

from trakt_api import (
    get_watch_history,
    get_ratings,
    get_watchlist
)

from database import (
    save_history_items,
    save_ratings,
    save_watchlist
)

from style import load_css
load_css()

st.title("🔄 Sync Data")

if st.button("Sync Full History"):

    with st.spinner("Downloading history..."):

        history = get_watch_history()

        save_history_items(history)

    st.success(
        f"Imported {len(history)} history items."
    )

st.divider()

if st.button("Sync Ratings"):

    with st.spinner("Downloading ratings..."):

        ratings = get_ratings()

        save_ratings(ratings)

    st.success(
        f"Imported {len(ratings)} ratings."
    )

st.divider()

if st.button("Sync Watchlist"):

    with st.spinner("Downloading watchlist..."):

        watchlist = get_watchlist()

        save_watchlist(watchlist)

    st.success(
        f"Imported {len(watchlist)} watchlist items."
    )    