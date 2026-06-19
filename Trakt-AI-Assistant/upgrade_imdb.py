import sqlite3

conn = sqlite3.connect("database.db")
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