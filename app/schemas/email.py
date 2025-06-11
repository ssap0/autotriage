from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime


class Email(BaseModel):
    """Email data model."""

    model_config = ConfigDict()

    id: int = Field(..., description="Unique email identifier")
    sender: str = Field(..., description="Email sender address")
    date: datetime = Field(..., description="Email date and time")
    mime_content: str = Field(..., description="Email content in MIME format")

    @field_serializer("date")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()


class EmailList(BaseModel):
    """List of emails response model."""

    emails: list[Email] = Field(..., description="List of emails")
    total: int = Field(..., description="Total number of emails")
