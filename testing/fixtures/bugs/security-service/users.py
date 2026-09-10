"""User management endpoints for the notes API."""
import sqlite3
from flask import request, jsonify, g
from app import app, get_db


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Fetch a user profile by id."""
    db = get_db()
    row = db.execute(
        "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@app.route("/users", methods=["POST"])
def create_user():
    """Register a new user."""
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "username or email already exists"}), 409
    return jsonify({"id": cur.lastrowid}), 201
