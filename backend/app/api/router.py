from app.api import auth, requests, services, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(services.router)
api_router.include_router(requests.router)
