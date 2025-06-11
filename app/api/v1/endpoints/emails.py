from fastapi import APIRouter

from app.schemas.email import Email
from app.utils.email_store import get_emails

router = APIRouter()


@router.get("/", response_model=list[Email])
async def get_all_emails() -> list[Email]:
    """
    Get all emails from the store.

    Returns:
        List of all emails
    """
    return get_emails()
