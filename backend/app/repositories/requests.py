from __future__ import annotations

from app.models.service_request import ServiceRequest
from sqlmodel import Session, select


def list_requests(
    session: Session, user_id: int, status: str | None = None
) -> list[ServiceRequest]:
    query = select(ServiceRequest).where(ServiceRequest.user_id == user_id)
    if status:
        query = query.where(ServiceRequest.status == status)
    return list(session.exec(query.order_by(ServiceRequest.created_at.desc())).all())


def get_request(session: Session, request_id: int, user_id: int) -> ServiceRequest | None:
    return session.exec(
        select(ServiceRequest).where(
            ServiceRequest.id == request_id, ServiceRequest.user_id == user_id
        )
    ).first()
