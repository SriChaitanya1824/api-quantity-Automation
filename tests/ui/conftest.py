from __future__ import annotations

import os

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from tests.utils.data_generator import unique_email


@pytest.fixture()
def ui_base_url(pytestconfig) -> str:
    return pytestconfig.getoption("base_url") or os.getenv("UI_BASE_URL", "http://localhost:5173")


@pytest.fixture()
def seeded_user() -> dict[str, str]:
    return {
        "email": os.getenv("TEST_USERNAME", "qa.user@example.com"),
        "password": os.getenv("TEST_PASSWORD", "Password123!"),
    }


@pytest.fixture()
def unique_ui_user() -> dict[str, str]:
    return {
        "email": unique_email("ui_user"),
        "password": "Password123!",
        "full_name": "UI Automation User",
        "department": "Quality Engineering",
    }


@pytest.fixture()
def logged_in_page(page, ui_base_url, seeded_user):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.login(seeded_user["email"], seeded_user["password"])
    DashboardPage(page).expect_loaded()
    return page
