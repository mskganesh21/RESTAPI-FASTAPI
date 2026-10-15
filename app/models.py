from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    """Request body for creating a note (like a Joi/Zod schema in Express)."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(default="", max_length=5000)


class NoteUpdate(BaseModel):
    """Partial update - all fields optional (like PATCH-style updates)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, max_length=5000)


class Note(BaseModel):
    """Full note returned from the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
