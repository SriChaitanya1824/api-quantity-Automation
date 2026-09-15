from __future__ import annotations

from datetime import datetime, timezone

from app.api.deps import current_user
from app.db.session import get_session
from app.models.service_request import RequestStatus, ServiceRequest
from app.models.user import User
from app.repositories.requests import get_request, list_requests
from app.repositories.services import get_service
from app.schemas.request import ServiceRequestCreate, ServiceRequestRead, ServiceRequestUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

router = APIRouter(prefix="/api/requests", tags=["requests"])

EDITABLE_STATUSES = {RequestStatus.open, RequestStatus.in_review}


@router.get("", response_model=list[ServiceRequestRead])
def read_requests(
    status_filter: RequestStatus | None = Query(default=None, alias="status"),
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    return list_requests(session, user.id, status_filter.value if status_filter else None)


@router.post("", response_model=ServiceRequestRead, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: ServiceRequestCreate,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    service = get_service(session, payload.service_id)
    if service is None or not service.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    request = ServiceRequest(user_id=user.id, **payload.model_dump())
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


@router.get("/{request_id}", response_model=ServiceRequestRead)
def read_request(
    request_id: int, user: User = Depends(current_user), session: Session = Depends(get_session)
):
    request = get_request(session, request_id, user.id)
    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request


@router.put("/{request_id}", response_model=ServiceRequestRead)
def update_request(
    request_id: int,
    payload: ServiceRequestUpdate,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    request = get_request(session, request_id, user.id)
    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    if request.status not in EDITABLE_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Request can no longer be updated"
        )
    updates = payload.model_dump(exclude_unset=True)
    if updates.get("status") == RequestStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Employees cannot complete requests"
        )
    for field, value in updates.items():
        setattr(request, field, value)
    request.updated_at = datetime.now(timezone.utc)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


@router.delete("/{request_id}", response_model=ServiceRequestRead)
def cancel_request(
    request_id: int, user: User = Depends(current_user), session: Session = Depends(get_session)
):
    request = get_request(session, request_id, user.id)
    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    if request.status not in EDITABLE_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Request cannot be cancelled"
        )
    request.status = RequestStatus.cancelled
    request.updated_at = datetime.now(timezone.utc)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request
