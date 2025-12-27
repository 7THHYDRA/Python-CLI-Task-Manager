from datetime import datetime


def validate_due_date(date_str):
    if not date_str:
        return None

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Due date must be in YYYY-MM-DD format")
