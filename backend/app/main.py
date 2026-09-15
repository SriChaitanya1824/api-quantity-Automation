from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI(title="Employee Access & Service Management API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok"}
