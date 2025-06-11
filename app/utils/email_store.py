import json
from typing import Optional
from pathlib import Path

from app.schemas.email import Email


def get_emails() -> list[Email]:
    """Get all emails from the JSON store.

    Returns:
        List of all emails
    """
    data_file = Path("data/emails.json")

    if not data_file.exists():
        return []

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Email(**email_data) for email_data in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def get_email_by_id(email_id: int) -> Optional[Email]:
    """Get a specific email by ID.

    Args:
        email_id: The ID of the email to retrieve

    Returns:
        Email object if found, None otherwise
    """
    emails = get_emails()
    return next((email for email in emails if email.id == email_id), None)
