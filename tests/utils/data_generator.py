from __future__ import annotations

from uuid import uuid4


def unique_email(prefix: str = "qa_user") -> str:
    return f"{prefix}_{uuid4().hex[:12]}@brivo-qa.example.com"


def valid_user(**overrides: str) -> dict[str, str]:
    data = {
        "email": unique_email(),
        "password": "Password123!",
        "full_name": "Automation Test User",
        "department": "Quality Engineering",
    }
    data.update(overrides)
    return data


def valid_request(service_id: int, **overrides: str | int) -> dict[str, str | int]:
    data: dict[str, str | int] = {
        "service_id": service_id,
        "title": "VPN access request",
        "description": "Please enable VPN access for regression testing.",
    }
    data.update(overrides)
    return data
