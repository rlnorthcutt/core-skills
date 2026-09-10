"""Simple note-keeping API with user-scoped notes."""
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DATABASE = "notes.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/notes", methods=["GET"])
def list_notes():
    user_id = request.args.get("user_id", type=int)
    db = get_db()
    rows = db.execute(
        "SELECT id, title, body FROM notes WHERE user_id = ?", (user_id,)
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    user_id = data["user_id"]
    title = data["title"]
    body = data.get("body", "")
    db = get_db()
    cur = db.execute(
        "INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
        (user_id, title, body),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201
