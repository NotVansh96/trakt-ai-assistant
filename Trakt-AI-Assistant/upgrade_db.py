import sqlite3

conn = sqlite3.connect("database.db")

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