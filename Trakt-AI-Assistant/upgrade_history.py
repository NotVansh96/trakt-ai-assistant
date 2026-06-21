import sqlite3

from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE history
    ADD COLUMN season INTEGER
    """)
    print("Added season column")
except:
    print("season column already exists")

try:
    cursor.execute("""
    ALTER TABLE history
    ADD COLUMN episode INTEGER
    """)
    print("Added episode column")
except:
    print("episode column already exists")

try:
    cursor.execute("""
    ALTER TABLE history
    ADD COLUMN episode_title TEXT
    """)
    print("Added episode_title column")
except:
    print("episode_title column already exists")

conn.commit()
conn.close()

print("History table upgraded successfully.")