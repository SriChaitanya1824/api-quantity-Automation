from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET", "test-secret-not-for-production")

from app.db.session import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Service  # noqa: E402

from tests.utils.api_client import APIClient  # noqa: E402
from tests.utils.data_generator import valid_request, valid_user  # noqa: E402


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(db_engine) -> Generator[Session, None, None]:
    SQLModel.metadata.drop_all(db_engine)
    SQLModel.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        session.add_all(
            [
                Service(
                    name="Building Access Badge",
                    category="Access",
                    description="Request or replace office entry badge.",
                ),
                Service(
                    name="VPN Access",
                    category="IT",
                    description="Request secure remote access for internal systems.",
                ),
            ]
        )
        session.commit()
        yield session


@pytest.fixture()
def api_client(session: Session) -> Generator[APIClient, None, None]:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        transport_client = httpx_client_adapter(client)
        yield APIClient("", transport_client)
    app.dependency_overrides.clear()


def httpx_client_adapter(test_client: TestClient):
    class Adapter:
        def request(self, method: str, url: str, **kwargs):
            return test_client.request(method, url, **kwargs)

    return Adapter()


@pytest.fixture()
def registered_user(api_client: APIClient) -> dict:
    user = valid_user()
    response = api_client.post("/api/auth/register", json=user)
    assert response.status_code == 201, response.text
    return user


@pytest.fixture()
def auth_token(api_client: APIClient, registered_user: dict) -> str:
    response = api_client.post(
        "/api/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture()
def authenticated_client(api_client: APIClient, auth_token: str) -> APIClient:
    return api_client.authenticated(auth_token)


@pytest.fixture()
def test_service(authenticated_client: APIClient) -> dict:
    response = authenticated_client.get("/api/services")
    assert response.status_code == 200, response.text
    return response.json()[0]


@pytest.fixture()
def test_request(authenticated_client: APIClient, test_service: dict) -> dict:
    response = authenticated_client.post("/api/requests", json=valid_request(test_service["id"]))
    assert response.status_code == 201, response.text
    return response.json()
