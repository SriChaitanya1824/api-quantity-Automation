import pytest

from tests.utils.assertions import (
    assert_error,
    assert_fields,
    assert_json_response,
    assert_list_response,
)

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_retrieve_services(authenticated_client):
    services = assert_list_response(authenticated_client.get("/api/services"), 200)

    assert len(services) >= 1
    assert all(service["active"] is True for service in services)


def test_services_response_has_expected_structure(authenticated_client):
    services = assert_list_response(authenticated_client.get("/api/services"), 200)

    for service in services:
        assert_fields(service, ["id", "name", "category", "description", "active"])
        assert isinstance(service["id"], int)
        assert isinstance(service["name"], str)
        assert service["name"]


def test_retrieve_single_service(authenticated_client, test_service):
    body = assert_json_response(
        authenticated_client.get(f"/api/services/{test_service['id']}"), 200
    )

    assert body["id"] == test_service["id"]
    assert body["name"] == test_service["name"]


def test_invalid_service_id_returns_not_found(authenticated_client):
    assert_error(authenticated_client.get("/api/services/99999"), 404, "service not found")


def test_services_require_authentication(api_client):
    assert_error(api_client.get("/api/services"), 401, "authentication required")
