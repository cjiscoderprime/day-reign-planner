from datetime import date
from pydantic import BaseModel, Field, field_validator


class MemoryInput(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    date: str
    content: str = Field(min_length=1, max_length=30000)

    @field_validator("date")
    @classmethod
    def valid_date(cls, value: str) -> str:
        date.fromisoformat(value)
        return value

    @field_validator("title", "content")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be empty")
        return value.strip()


class MemoryResponse(MemoryInput):
    id: str
    createdAt: str
    updatedAt: str
