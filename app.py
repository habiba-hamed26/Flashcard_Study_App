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


def insert_cards(conn, deck_id, questions, answers):
    #Insert every non empty pair. returns total added.
    added = 0
    for question, answer in zip(questions, answers):
        question = question.strip()
        answer = answer.strip()
        if question and answer:     #  insert into DB only if both question and answer contain text
            conn.execute("INSERT INTO cards (deck_id, question, answer) VALUES (?, ?, ?)",(deck_id, question, answer),)
            added += 1
    return added

# route to create a new deck
@app.route("/deck/new", methods=["GET", "POST"])
def new_deck():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Deck name is required.")
            return redirect(url_for("new_deck"))
 
        conn = get_db_connection()
        cursor = conn.execute("INSERT INTO decks (name) VALUES (?)", (name,)) 
        deck_id = cursor.lastrowid
    
        questions = request.form.getlist("questions[]")
        answers = request.form.getlist("answers[]")
        added = insert_cards(conn, deck_id, questions, answers)
 
        conn.commit()
        conn.close()
 
        if added:
            flash(f"Deck created with {added} card{'s' if added != 1 else ''}!")
        else:
            flash("Deck created!")
        return redirect(url_for("view_deck", deck_id=deck_id))
 
    return render_template("new_deck.html")   # show the form to create a new deck 


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

# Route to delete a specific deck 
@app.route("/deck/<int:deck_id>/delete", methods=["POST"])
def delete_deck(deck_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))  # Delete the deck from the database by its ID
    conn.commit()
    conn.close()
    return redirect(url_for("index"))   # Redirect to the home page

# Card routes
 # route to add a new card to a specific deck
@app.route("/deck/<int:deck_id>/add", methods=["GET", "POST"])
def add_card(deck_id):
    conn = get_db_connection()
    deck = conn.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
    if deck is None:
        conn.close()
        abort(404)
 
    if request.method == "POST":
        questions = request.form.getlist("questions[]")
        answers = request.form.getlist("answers[]")
        added = insert_cards(conn, deck_id, questions, answers)
        conn.commit()
        conn.close()
 
        if added:
            flash(f"{added} card{'s' if added != 1 else ''} added!")
        else:
            flash("No cards added — fill in at least one question and answer.")
        return redirect(url_for("view_deck", deck_id=deck_id))
 
    conn.close()
    return render_template("add_card.html", deck=deck)
 

 # route to delete a card from a deck
@app.route("/card/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id):
    conn = get_db_connection()
    card = conn.execute("SELECT deck_id FROM cards WHERE id = ?", (card_id,)).fetchone() # get the card with the specified id
    if card is None:
        conn.close()
        abort(404)
    deck_id = card["deck_id"] # get the deck id of the card to redirect back to the deck view after deletion
    conn.execute("DELETE FROM cards WHERE id = ?", (card_id,)) # delete the card from the database by its ID
    conn.commit()
    conn.close()
    return redirect(url_for("view_deck", deck_id=deck_id))
 
 
if __name__ == "__main__":
    app.run(debug=True)
 