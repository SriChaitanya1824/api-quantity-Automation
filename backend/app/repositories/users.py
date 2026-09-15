from __future__ import annotations

from app.models.user import User
from sqlmodel import Session, select


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)
