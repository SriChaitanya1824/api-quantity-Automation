from __future__ import annotations

import os
from uuid import uuid4

from locust import HttpUser, between, task


class EmployeePortalUser(HttpUser):
    wait_time = between(1, 3)
    host = os.getenv("API_BASE_URL", "http://localhost:8000")
    token: str | None = None
    service_id: int | None = None

    def on_start(self) -> None:
        email = f"locust_{uuid4().hex[:10]}@brivo-qa.example.com"
        password = "Password123!"
        self.client.post(
            "/api/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Locust Test User",
                "department": "Quality Engineering",
            },
            timeout=10,
        )
        login_response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        if login_response.ok:
            self.token = login_response.json()["access_token"]
        services_response = self.client.get("/api/services", headers=self.auth_headers, timeout=10)
        if services_response.ok and services_response.json():
            self.service_id = services_response.json()[0]["id"]

    @property
    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def get_services(self) -> None:
        self.client.get("/api/services", headers=self.auth_headers, timeout=10)

    @task(3)
    def get_requests(self) -> None:
        self.client.get("/api/requests", headers=self.auth_headers, timeout=10)

    @task(1)
    def create_request(self) -> None:
        if not self.service_id:
            return
        self.client.post(
            "/api/requests",
            headers=self.auth_headers,
            json={
                "service_id": self.service_id,
                "title": "Performance smoke request",
                "description": "Created by Locust during a local performance smoke test.",
            },
            timeout=10,
        )
