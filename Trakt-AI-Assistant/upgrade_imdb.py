import sqlite3

from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE history
    ADD COLUMN imdb_id TEXT
    """)
    print("imdb_id added")
except:
    print("imdb_id already exists")

conn.commit()
conn.close()