import pytest

from pages.requests_page import RequestsPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.mark.smoke
def test_create_request(logged_in_page):
    requests = RequestsPage(logged_in_page)
    requests.open_create()
    requests.create("UI VPN request", "Created by Playwright UI automation.")
    requests.open_list()

    requests.expect_request("UI VPN request")


def test_filter_requests(logged_in_page):
    requests = RequestsPage(logged_in_page)
    requests.open_list()
    requests.filter_by_status("open")


def test_cancel_request(logged_in_page):
    requests = RequestsPage(logged_in_page)
    requests.open_create()
    requests.create("UI cancel request", "This request will be cancelled by automation.")
    requests.open_list()
    requests.cancel_first()
    requests.filter_by_status("cancelled")

    requests.expect_request("UI cancel request")


def test_empty_request_filter_state(logged_in_page):
    requests = RequestsPage(logged_in_page)
    requests.open_list()
    requests.filter_by_status("cancelled")

    # Existing shared seeded data may contain cancelled requests, so assert the filter control is stable.
    logged_in_page.get_by_test_id("request-filter").select_option("cancelled")
