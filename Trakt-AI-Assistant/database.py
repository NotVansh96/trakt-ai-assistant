import sqlite3

from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        trakt_id INTEGER PRIMARY KEY,
        title TEXT,
        media_type TEXT,
        watched_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        trakt_id INTEGER PRIMARY KEY,
        title TEXT,
        media_type TEXT,
        rating INTEGER,
        rated_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
    trakt_id INTEGER PRIMARY KEY,
    title TEXT,
    media_type TEXT,
    listed_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taste_profile (
    id INTEGER PRIMARY KEY,
    profile TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_history_items(items):

    conn = get_connection()
    cursor = conn.cursor()

    for item in items:

        media_type = item["type"]

        season = None
        episode = None
        episode_title = None
        imdb_id = None

        if media_type == "movie":

            trakt_id = item["movie"]["ids"]["trakt"]

            title = item["movie"]["title"]

            imdb_id = item["movie"]["ids"].get(
                "imdb"
            )

        elif media_type == "episode":

            trakt_id = item["episode"]["ids"]["trakt"]

            title = item["show"]["title"]

            imdb_id = item["show"]["ids"].get(
                "imdb"
            )

            season = item["episode"].get(
                "season"
            )

            episode = item["episode"].get(
                "number"
            )

            episode_title = item["episode"].get(
                "title"
            )

        else:
            continue

        cursor.execute("""
        INSERT OR REPLACE INTO history
        (
            trakt_id,
            title,
            media_type,
            watched_at,
            season,
            episode,
            episode_title,
            imdb_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trakt_id,
            title,
            media_type,
            item["watched_at"],
            season,
            episode,
            episode_title,
            imdb_id
        ))

    conn.commit()
    conn.close()


def get_database_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM history")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE media_type='movie'"
    )
    movies = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE media_type='episode'"
    )
    episodes = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "movies": movies,
        "episodes": episodes
    }


def get_recent_history(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, media_type, watched_at
    FROM history
    ORDER BY watched_at DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows    


def count_history_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM history"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total    


def save_ratings(items):
    conn = get_connection()
    cursor = conn.cursor()

    for item in items:

        media_type = item["type"]

        if media_type == "movie":
            trakt_id = item["movie"]["ids"]["trakt"]
            title = item["movie"]["title"]

        elif media_type == "show":
            trakt_id = item["show"]["ids"]["trakt"]
            title = item["show"]["title"]

        else:
            continue

        cursor.execute("""
        INSERT OR REPLACE INTO ratings
        (trakt_id, title, media_type, rating, rated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            trakt_id,
            title,
            media_type,
            item["rating"],
            item["rated_at"]
        ))

    conn.commit()
    conn.close()    


def get_top_ratings(limit=100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, rating
    FROM ratings
    ORDER BY rating DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows    


def save_watchlist(items):
    conn = get_connection()
    cursor = conn.cursor()

    for item in items:

        media_type = item["type"]

        if media_type == "movie":
            trakt_id = item["movie"]["ids"]["trakt"]
            title = item["movie"]["title"]

        elif media_type == "show":
            trakt_id = item["show"]["ids"]["trakt"]
            title = item["show"]["title"]

        else:
            continue

        cursor.execute("""
        INSERT OR REPLACE INTO watchlist
        (trakt_id, title, media_type, listed_at)
        VALUES (?, ?, ?, ?)
        """, (
            trakt_id,
            title,
            media_type,
            item["listed_at"]
        ))

    conn.commit()
    conn.close()


def get_watchlist_items(limit=200):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, media_type
    FROM watchlist
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows    


def get_top_rated(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, rating
    FROM ratings
    ORDER BY rating DESC, title ASC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_rating_distribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT rating, COUNT(*)
    FROM ratings
    GROUP BY rating
    ORDER BY rating
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_most_watched_shows(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, COUNT(*) as episodes
    FROM history
    WHERE media_type='episode'
    GROUP BY title
    ORDER BY episodes DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_all_watchlist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, media_type
    FROM watchlist
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows    


def save_taste_profile(profile):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM taste_profile
    """)

    cursor.execute("""
    INSERT INTO taste_profile
    (profile)
    VALUES (?)
    """, (profile,))

    conn.commit()
    conn.close()


def get_taste_profile():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT profile
    FROM taste_profile
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return ""    


def get_recent_movies(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        title,
        watched_at,
        imdb_id
    FROM history
    WHERE media_type='movie'
    ORDER BY watched_at DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_recent_episodes(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        title,
        season,
        episode,
        episode_title
    FROM history
    WHERE media_type='episode'
    ORDER BY watched_at DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_watchlist_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM watchlist"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_rating_distribution_by_type():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        rating,
        media_type,
        COUNT(*)
    FROM ratings
    GROUP BY rating, media_type
    ORDER BY rating
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_watchtime_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM history
    WHERE media_type='movie'
    """)

    movie_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM history
    WHERE media_type='episode'
    """)

    episode_count = cursor.fetchone()[0]

    conn.close()

    # temporary estimates

    movie_minutes = movie_count * 120
    episode_minutes = episode_count * 24

    total_minutes = movie_minutes + episode_minutes

    return {
        "movies_minutes": movie_minutes,
        "episodes_minutes": episode_minutes,
        "total_minutes": total_minutes
    }


def get_last_30_days_watchtime():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT media_type
    FROM history
    WHERE watched_at >= datetime('now', '-30 days')
    """)

    rows = cursor.fetchall()

    conn.close()

    movie_minutes = 0
    episode_minutes = 0

    for (media_type,) in rows:

        if media_type == "movie":
            movie_minutes += 120

        elif media_type == "episode":
            episode_minutes += 24

    return movie_minutes + episode_minutes


def get_last_7_days_activity():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DATE(watched_at), COUNT(*)
    FROM history
    WHERE watched_at >= datetime('now', '-7 days')
    GROUP BY DATE(watched_at)
    ORDER BY DATE(watched_at)
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows