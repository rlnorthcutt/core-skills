import sqlite3
import app as note_app


def setup_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "notes.db")
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, user_id INT, title TEXT, body TEXT)")
    conn.commit()
    monkeypatch.setattr(note_app, "DATABASE", db_path)
    return db_path


def test_create_and_list(tmp_path, monkeypatch):
    setup_db(tmp_path, monkeypatch)
    client = note_app.app.test_client()
    r = client.post("/notes", json={"user_id": 1, "title": "T", "body": "B"})
    assert r.status_code == 201
    r = client.get("/notes?user_id=1")
    assert len(r.get_json()) == 1
