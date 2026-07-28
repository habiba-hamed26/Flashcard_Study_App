import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for, abort

app = Flask(__name__)
app.secret_key = 'my-flashcard-app-2026'
 
 
def get_db_connection():
    conn = sqlite3.connect('flashcard_database.db')
    conn.execute('PRAGMA foreign_keys = ON')   # Enable foreign key constraints
    conn.row_factory = sqlite3.Row             # Set row factory to return rows as dictionaries
    return conn
 

# Home page route which displays all decks
@app.route("/")
def index():
    conn = get_db_connection()
    # get all decks with their card counts
    decks = conn.execute(
        """SELECT decks.id, decks.name, COUNT(cards.id) AS card_count
           FROM decks
           LEFT JOIN cards ON cards.deck_id = decks.id
           GROUP BY decks.id
           ORDER BY decks.id"""
    ).fetchall()
    conn.close()
    return render_template("index.html", decks=decks)

# Route to create a new deck
@app.route("/deck/new", methods=["GET", "POST"])
def new_deck():
    if request.method == "POST":   # 
        name = request.form.get("name", "").strip()     # get the deck name 
        if name:
            conn = get_db_connection()
            conn.execute("INSERT INTO decks (name) VALUES (?)", (name,))  # insert the new deck into the database
            conn.commit()
            flash(f"Deck '{name}' created successfully!", "success")
            conn.close()
        return redirect(url_for("index"))
    return render_template("new_deck.html") # show the form to create a new deck


# Route to view a specific deck and its cards
@app.route("/deck/<int:deck_id>")
def view_deck(deck_id):
    conn = get_db_connection()
    # get the deck with the specified id
    deck = conn.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
    if deck is None:
        conn.close()
        abort(404)

    # Get all cards that belong to this deck
    cards = conn.execute("SELECT * FROM cards WHERE deck_id = ? ORDER BY id", (deck_id,) ).fetchall()
    conn.close()
    return render_template("deck.html", deck=deck, cards=cards)