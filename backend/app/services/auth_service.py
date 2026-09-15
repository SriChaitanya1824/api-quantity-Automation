from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import get_user_by_email
from app.schemas.auth import LoginRequest, RegisterRequest
from fastapi import HTTPException, status
from sqlmodel import Session


def register_user(session: Session, payload: RegisterRequest) -> User:
    if get_user_by_email(session, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
        )
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        department=payload.department,
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def login_user(session: Session, payload: LoginRequest) -> str:
    user = get_user_by_email(session, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    return create_access_token(str(user.id))
