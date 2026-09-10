from custom_apps import action

@action
def get_message(name: str) -> dict:
    if not isinstance(name, str) or not name:
        return {"ok": False, "error": "name must be a non-empty string"}
    return {"ok": True, "message": f"Hello {name}"}
