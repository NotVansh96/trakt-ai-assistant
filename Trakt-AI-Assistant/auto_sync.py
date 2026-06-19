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


def auto_sync():

    history = get_watch_history()
    save_history_items(history)

    ratings = get_ratings()
    save_ratings(ratings)

    watchlist = get_watchlist()
    save_watchlist(watchlist)