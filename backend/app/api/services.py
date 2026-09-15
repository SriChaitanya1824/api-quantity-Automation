from app.api.deps import current_user
from app.db.session import get_session
from app.repositories.services import get_service, list_active_services
from app.schemas.service import ServiceRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

router = APIRouter(prefix="/api/services", tags=["services"], dependencies=[Depends(current_user)])


@router.get("", response_model=list[ServiceRead])
def list_services(session: Session = Depends(get_session)):
    return list_active_services(session)


@router.get("/{service_id}", response_model=ServiceRead)
def read_service(service_id: int, session: Session = Depends(get_session)):
    service = get_service(session, service_id)
    if service is None or not service.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service
