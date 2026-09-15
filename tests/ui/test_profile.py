import pytest
from playwright.sync_api import expect

from pages.profile_page import ProfilePage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


def test_view_profile(logged_in_page):
    profile = ProfilePage(logged_in_page)
    profile.open()

    profile.expect_values("QA Portfolio User", "Quality Engineering")


@pytest.mark.smoke
def test_update_profile(logged_in_page):
    profile = ProfilePage(logged_in_page)
    profile.open()
    profile.update("QA Portfolio User", "Quality Engineering")

    profile.expect_values("QA Portfolio User", "Quality Engineering")


def test_invalid_profile_information_uses_browser_validation(logged_in_page):
    profile = ProfilePage(logged_in_page)
    profile.open()
    logged_in_page.get_by_test_id("profile-name").fill("A")
    logged_in_page.get_by_test_id("profile-save").click()

    expect(logged_in_page.get_by_test_id("profile-name")).not_to_have_js_property(
        "validationMessage", ""
    )
