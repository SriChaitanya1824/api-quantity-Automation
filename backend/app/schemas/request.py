from __future__ import annotations

from app.models.service_request import RequestStatus
from pydantic import BaseModel, Field


class ServiceRequestCreate(BaseModel):
    service_id: int = Field(gt=0)
    title: str = Field(min_length=5, max_length=160)
    description: str = Field(min_length=10, max_length=1000)


class ServiceRequestUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=160)
    description: str | None = Field(default=None, min_length=10, max_length=1000)
    status: RequestStatus | None = None


class ServiceRequestRead(BaseModel):
    id: int
    user_id: int
    service_id: int
    title: str
    description: str
    status: RequestStatus
