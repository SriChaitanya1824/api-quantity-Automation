from __future__ import annotations

import logging
from typing import Any

import httpx

LOGGER = logging.getLogger(__name__)


class APIClient:
    def __init__(
        self,
        base_url: str,
        client: httpx.Client,
        token: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.token = token
        self.timeout = timeout

    def authenticated(self, token: str) -> APIClient:
        return APIClient(self.base_url, self.client, token=token, timeout=self.timeout)

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("DELETE", path, **kwargs)

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = dict(kwargs.pop("headers", {}) or {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        response = self.client.request(
            method,
            f"{self.base_url}{path}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        LOGGER.info("%s %s -> %s", method, path, response.status_code)
        return response
