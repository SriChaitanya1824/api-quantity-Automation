from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class RequestStatus(str, Enum):
    open = "open"
    in_review = "in_review"
    approved = "approved"
    cancelled = "cancelled"
    completed = "completed"


class ServiceRequest(SQLModel, table=True):
    __tablename__ = "service_requests"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    service_id: int = Field(foreign_key="services.id", nullable=False)
    title: str = Field(nullable=False, min_length=5, max_length=160)
    description: str = Field(nullable=False, min_length=10, max_length=1000)
    status: RequestStatus = Field(default=RequestStatus.open, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
