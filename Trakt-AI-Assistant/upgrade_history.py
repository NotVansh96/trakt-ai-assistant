import sqlite3

conn = sqlite3.connect("database.db")
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