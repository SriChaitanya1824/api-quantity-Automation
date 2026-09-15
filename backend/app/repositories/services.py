from __future__ import annotations

from app.models.service import Service
from sqlmodel import Session, select


def list_active_services(session: Session) -> list[Service]:
    return list(
        session.exec(select(Service).where(Service.active.is_(True)).order_by(Service.name)).all()
    )


def get_service(session: Session, service_id: int) -> Service | None:
    return session.get(Service, service_id)
