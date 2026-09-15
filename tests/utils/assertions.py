from __future__ import annotations

from collections.abc import Iterable

import httpx


def assert_json_response(response: httpx.Response, status_code: int) -> dict:
    assert response.status_code == status_code, response.text
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    assert isinstance(body, dict)
    return body


def assert_list_response(response: httpx.Response, status_code: int) -> list:
    assert response.status_code == status_code, response.text
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    assert isinstance(body, list)
    return body


def assert_fields(body: dict, fields: Iterable[str]) -> None:
    for field in fields:
        assert field in body, f"Missing field: {field}"


def assert_error(
    response: httpx.Response, status_code: int, message_fragment: str | None = None
) -> dict:
    body = assert_json_response(response, status_code)
    assert "detail" in body
    if message_fragment:
        assert message_fragment.lower() in str(body["detail"]).lower()
    return body
