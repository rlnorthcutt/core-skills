"""Focus Timer backend actions.

Stateless actions; all state persists to data/sessions.json.
Each invocation runs in a fresh subprocess, so we read/write the file each call.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from custom_apps import action

DATA_DIR = Path(__file__).resolve().parent / "data"
SESSIONS_FILE = DATA_DIR / "sessions.json"


def _load_sessions() -> list[dict[str, Any]]:
    if not SESSIONS_FILE.exists():
        return []
    try:
        data = json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def _save_sessions(sessions: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


@action
def log_session(duration_minutes: int, started_at: str | None = None) -> dict[str, Any]:
    """Record one completed focus session. duration_minutes must be a positive int."""
    if not isinstance(duration_minutes, int) or isinstance(duration_minutes, bool):
        return {"ok": False, "error": "duration_minutes must be an integer"}
    if duration_minutes <= 0 or duration_minutes > 600:
        return {"ok": False, "error": "duration_minutes must be between 1 and 600"}

    if started_at:
        try:
            started = datetime.fromisoformat(started_at)
        except ValueError:
            return {"ok": False, "error": f"invalid started_at: {started_at!r}"}
        day = started.astimezone(timezone.utc).date().isoformat()
    else:
        day = date.today().isoformat()

    sessions = _load_sessions()
    record = {
        "id": len(sessions) + 1,
        "duration_minutes": duration_minutes,
        "day": day,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }
    sessions.append(record)
    _save_sessions(sessions)
    return {"ok": True, "session": record}


@action
def get_today_total() -> dict[str, Any]:
    """Return today's total focus time in minutes and the session count."""
    today = date.today().isoformat()
    sessions = _load_sessions()
    todays = [s for s in sessions if s.get("day") == today]
    total = sum(int(s.get("duration_minutes", 0)) for s in todays)
    return {"ok": True, "day": today, "total_minutes": total, "session_count": len(todays)}
