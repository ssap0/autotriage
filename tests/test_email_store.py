from uuid import UUID
from app.utils.email_store import get_emails, get_email_by_id
from app.schemas.email import Email


def test_get_emails():
    """Test getting all emails."""
    emails = get_emails()
    assert isinstance(emails, list)

    if emails:  # If emails exist in the data file
        assert len(emails) > 0
        assert all(isinstance(email, Email) for email in emails)


def test_get_email_by_id():
    """Test getting a specific email by ID."""
    emails = get_emails()

    if emails:  # If emails exist
        # Test getting first email
        first_email = get_email_by_id(emails[0].id)
        assert first_email is not None
        assert first_email.id == emails[0].id

    # Test getting non-existent email
    non_existent_id = UUID("00000000-0000-0000-0000-000000000000")
    email = get_email_by_id(non_existent_id)
    assert email is None
