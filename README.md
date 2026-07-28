# Flashcard Study App

A simple Flask and SQLite flashcard app. The flip animation is pure CSS

## Project structure
```
flashcard_app/
 app.py              # Flask routes
 init_database.py    # Creates flashcard_database.db from schema.sql
 schema.sql           # Table definitions (decks, cards)
 flashcard_database.db          # SQLite file (created after running init_database.py)
 templates/
   base.html
   index.html       # List of decks
   new_deck.html    # Create a deck
   deck.html         # Study view (flip cards)
   add_card.html    # Add a card to a deck
 static/
    style.css         # Layout + flip animation
```

## Setup

1. Install Flask:
   ```
   pip install flask
   ```

2. Initialize the database (creates `flashcard_database.db`):
   ```
   python init_database.py
   ```
 
3. Run the app:
   ```
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000`

## How it works

- **Create a deck** from the homepage.
- **Add cards** question/answer pairs to a deck.
- **Click a card** in the study view it flips via CSS to reveal the answer.
- **Delete** individual cards or entire decks.

## Database schema

```sql
decks(id, name)
cards(id, deck_id -> decks.id, question, answer)
```
