from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=120)
    category: str = Field(nullable=False, max_length=80)
    description: str = Field(nullable=False, max_length=500)
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
