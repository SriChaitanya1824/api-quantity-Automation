from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    department: str


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    department: str | None = Field(default=None, min_length=2, max_length=80)
