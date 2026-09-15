import pytest

from pages.services_page import ServicesPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.smoke
def test_view_service_catalog(logged_in_page):
    services = ServicesPage(logged_in_page)
    services.open()

    services.expect_service_cards()


def test_select_service_from_create_request(logged_in_page):
    logged_in_page.get_by_test_id("nav-create").click()

    logged_in_page.get_by_test_id("request-service").select_option(index=0)
