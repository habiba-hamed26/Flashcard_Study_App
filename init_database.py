import sqlite3

conn = sqlite3.connect('flashcard_database.db')
with open('schema.sql') as f:
    conn.executescript(f.read())


decks = {
    "Python Basics": [
        ("What keyword defines a function in Python?", "def"),
        ("What data type is {}?", "Dictionary"),
        ("What does len() do?", "Returns the length of a sequence"),
        ("How do you comment a line in Python?", "Using #"),
        ("What does == check for?", "Equality"),
    ],
    "World Capitals": [
        ("Capital of Japan", "Tokyo"),
        ("Capital of Egypt", "Cairo"),
        ("Capital of Canada", "Ottawa"),
        ("Capital of Australia", "Canberra"),
        ("Capital of Brazil", "Brasília"),
    ],
    "Human Body Systems": [
        ("Organ that pumps blood", "Heart"),
        ("Organ responsible for filtering blood", "Kidneys"),
        ("Largest organ in the body", "Skin"),
        ("Gas exchanged in the lungs", "Oxygen and carbon dioxide"),
        ("System that carries messages via neurons", "Nervous system"),
    ],
}

for deck_name, cards in decks.items():
    cursor = conn.execute("INSERT INTO decks (name) VALUES (?)", (deck_name,))
    deck_id = cursor.lastrowid
    conn.executemany(
        "INSERT INTO cards (deck_id, question, answer) VALUES (?, ?, ?)",
        [(deck_id, q, a) for q, a in cards]
    )

conn.commit()
conn.close()

