import sqlite3

conn = sqlite3.connect('flashcard_database.db')
with open('schema.sql') as f:
    conn.executescript(f.read())
conn.close()

