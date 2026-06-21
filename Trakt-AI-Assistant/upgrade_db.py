import sqlite3

from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS taste_profile (
    id INTEGER PRIMARY KEY,
    profile TEXT
)
""")

conn.commit()

conn.close()

print("Database upgraded successfully.")