import pytest
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.smoke
def test_valid_login(page, ui_base_url, seeded_user):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.login(seeded_user["email"], seeded_user["password"])

    DashboardPage(page).expect_loaded()


def test_invalid_password_shows_error(page, ui_base_url, seeded_user):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.login(seeded_user["email"], "WrongPassword123!")

    login.expect_error("Invalid email or password")


def test_unknown_user_shows_error(page, ui_base_url):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.login("unknown@brivo-qa.example.com", "Password123!")

    login.expect_error("Invalid email or password")


def test_empty_email_uses_browser_validation(page, ui_base_url):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.email.fill("")
    login.password.fill("Password123!")
    login.submit.click()

    expect(login.email).not_to_have_js_property("validationMessage", "")


def test_empty_password_uses_browser_validation(page, ui_base_url, seeded_user):
    login = LoginPage(page, ui_base_url)
    login.goto()
    login.email.fill(seeded_user["email"])
    login.password.fill("")
    login.submit.click()

    expect(login.password).not_to_have_js_property("validationMessage", "")


def test_logout_returns_to_login(logged_in_page):
    DashboardPage(logged_in_page).logout()
