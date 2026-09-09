#!/usr/bin/env python3
"""Validate Omnideck SkillRecord JSON files.

Checks the schema Omnideck's skill loader expects:
  id: str, name: str (unique, verb-first kebab-case recommended),
  description: str, prompt: str, tool_categories: list[str]

Usage: validate.py skills/*/skill.json
"""
import json
import sys
from pathlib import Path

VALID_CATEGORIES = {
    "coding", "browser", "webfetch", "memory", "planning",
    "image_generation", "music_generation", "desktop",
    "email", "calendar", "drive", "contacts", "http",
}

def check(path: Path) -> list[str]:
    errors = []
    try:
        rec = json.loads(path.read_text())
    except Exception as e:
        return [f"{path}: invalid JSON: {e}"]

    for field in ("id", "name", "description", "prompt"):
        if not rec.get(field):
            errors.append(f"{path}: missing or empty '{field}'")
    if not isinstance(rec.get("tool_categories"), list):
        errors.append(f"{path}: 'tool_categories' must be a list")

    rid, name = rec.get("id", ""), rec.get("name", "")
    if rid and name and rid != name:
        errors.append(f"{path}: id ({rid!r}) != name ({name!r}) — convention is id == name")
    for n in (rid, name):
        if n and (" " in n or n != n.lower() or not n.replace("-", "").replace("_", "").isalnum()):
            errors.append(f"{path}: name/id {n!r} not kebab-case")
    for cat in rec.get("tool_categories", []):
        if cat not in VALID_CATEGORIES:
            errors.append(f"{path}: unknown tool category {cat!r}")
    return errors

def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        print(__doc__)
        return 2
    all_errors = []
    for p in paths:
        all_errors += check(p)
    if all_errors:
        print("\n".join(all_errors))
        return 1
    print(f"OK: {len(paths)} skill record(s) valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
