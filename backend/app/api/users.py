from datetime import datetime, timezone

from app.api.deps import current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(user: User = Depends(current_user)):
    return user


@router.put("/me", response_model=UserRead)
def update_me(
    payload: UserUpdate, user: User = Depends(current_user), session: Session = Depends(get_session)
):
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
