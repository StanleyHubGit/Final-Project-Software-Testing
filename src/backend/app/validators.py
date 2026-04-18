from datetime import datetime

VALID_STATUSES = ["pending", "submitted", "late"]


def validate_title(title):
    if not title:
        raise ValueError("Title is required")

    if not isinstance(title, str):
        raise ValueError("Title must be a string")

    if title.strip() == "":
        raise ValueError("Title cannot be empty")

    return title.strip()


def validate_status(status):
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status. Must be one of {VALID_STATUSES}")

    return status


def validate_deadline(deadline):
    if deadline is None:
        return None

    try:
        datetime.fromisoformat(deadline)
    except Exception:
        raise ValueError("Invalid deadline format")

    return deadline


def validate_user_id(user_id):
    if not user_id:
        raise ValueError("User ID is required")

    if not isinstance(user_id, int):
        raise ValueError("User ID must be integer")

    return user_id