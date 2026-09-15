import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.register_page import RegisterPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.smoke
def test_successful_registration(page, ui_base_url, unique_ui_user):
    LoginPage(page, ui_base_url).goto()
    register = RegisterPage(page)
    register.open_from_login()
    register.register(**unique_ui_user)

    register.expect_success()


def test_duplicate_registration_shows_error(page, ui_base_url, seeded_user):
    LoginPage(page, ui_base_url).goto()
    register = RegisterPage(page)
    register.open_from_login()
    register.register("Duplicate User", seeded_user["email"], seeded_user["password"])

    expect(page.get_by_role("alert")).to_contain_text("already registered")


def test_invalid_registration_email_uses_browser_validation(page, ui_base_url):
    LoginPage(page, ui_base_url).goto()
    register = RegisterPage(page)
    register.open_from_login()
    register.register("Bad Email", "not-an-email", "Password123!")

    expect(page.get_by_test_id("register-email")).not_to_have_js_property("validationMessage", "")


def test_short_registration_password_uses_browser_validation(page, ui_base_url, unique_ui_user):
    LoginPage(page, ui_base_url).goto()
    register = RegisterPage(page)
    register.open_from_login()
    register.register(unique_ui_user["full_name"], unique_ui_user["email"], "short")

    expect(page.get_by_test_id("register-password")).not_to_have_js_property(
        "validationMessage", ""
    )
