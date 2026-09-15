import pytest

from tests.utils.assertions import (
    assert_error,
    assert_fields,
    assert_json_response,
    assert_list_response,
)
from tests.utils.data_generator import valid_request, valid_user

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_create_service_request(authenticated_client, test_service):
    payload = valid_request(test_service["id"], title="Badge replacement")

    body = assert_json_response(authenticated_client.post("/api/requests", json=payload), 201)

    assert_fields(body, ["id", "user_id", "service_id", "title", "description", "status"])
    assert body["service_id"] == test_service["id"]
    assert body["title"] == "Badge replacement"
    assert body["status"] == "open"


def test_retrieve_all_requests(authenticated_client, test_request):
    requests = assert_list_response(authenticated_client.get("/api/requests"), 200)

    assert any(item["id"] == test_request["id"] for item in requests)


def test_retrieve_one_request(authenticated_client, test_request):
    body = assert_json_response(
        authenticated_client.get(f"/api/requests/{test_request['id']}"), 200
    )

    assert body["id"] == test_request["id"]
    assert body["title"] == test_request["title"]


def test_update_request(authenticated_client, test_request):
    body = assert_json_response(
        authenticated_client.put(
            f"/api/requests/{test_request['id']}",
            json={"title": "Updated request title", "description": "Updated request description."},
        ),
        200,
    )

    assert body["id"] == test_request["id"]
    assert body["title"] == "Updated request title"
    assert body["description"] == "Updated request description."


def test_cancel_request(authenticated_client, test_request):
    body = assert_json_response(
        authenticated_client.delete(f"/api/requests/{test_request['id']}"), 200
    )

    assert body["id"] == test_request["id"]
    assert body["status"] == "cancelled"


def test_filter_requests_by_status(authenticated_client, test_request):
    authenticated_client.delete(f"/api/requests/{test_request['id']}")

    cancelled = assert_list_response(
        authenticated_client.get("/api/requests?status=cancelled"), 200
    )
    open_requests = assert_list_response(authenticated_client.get("/api/requests?status=open"), 200)

    assert any(item["id"] == test_request["id"] for item in cancelled)
    assert all(item["status"] == "open" for item in open_requests)


def test_invalid_request_id_returns_not_found(authenticated_client):
    assert_error(authenticated_client.get("/api/requests/99999"), 404, "request not found")


def test_requests_require_authentication(api_client):
    assert_error(api_client.get("/api/requests"), 401, "authentication required")


def test_user_cannot_access_another_users_request(api_client, authenticated_client, test_service):
    first_request = assert_json_response(
        authenticated_client.post("/api/requests", json=valid_request(test_service["id"])),
        201,
    )
    second_user = valid_user()
    api_client.post("/api/auth/register", json=second_user)
    token = api_client.post(
        "/api/auth/login",
        json={"email": second_user["email"], "password": second_user["password"]},
    ).json()["access_token"]

    assert_error(
        api_client.authenticated(token).get(f"/api/requests/{first_request['id']}"),
        404,
        "request not found",
    )


def test_employee_cannot_complete_request(authenticated_client, test_request):
    assert_error(
        authenticated_client.put(
            f"/api/requests/{test_request['id']}",
            json={"status": "completed"},
        ),
        403,
        "cannot complete",
    )


def test_cancelled_request_cannot_be_updated(authenticated_client, test_request):
    authenticated_client.delete(f"/api/requests/{test_request['id']}")

    assert_error(
        authenticated_client.put(
            f"/api/requests/{test_request['id']}",
            json={"title": "Too late to edit"},
        ),
        409,
        "no longer be updated",
    )


@pytest.mark.parametrize(
    "payload, field",
    [
        ({"title": "Missing service", "description": "Missing service id."}, "service_id"),
        ({"service_id": 1, "description": "Missing title."}, "title"),
        ({"service_id": 1, "title": "Short", "description": "short"}, "description"),
        (
            {
                "service_id": 0,
                "title": "Bad service",
                "description": "Service id must be positive.",
            },
            "service_id",
        ),
    ],
)
def test_invalid_request_payloads_return_validation_errors(authenticated_client, payload, field):
    body = assert_error(authenticated_client.post("/api/requests", json=payload), 422)

    assert field in str(body["detail"])


def test_request_boundary_values_are_accepted(authenticated_client, test_service):
    payload = valid_request(
        test_service["id"],
        title="T" * 160,
        description="D" * 1000,
    )

    body = assert_json_response(authenticated_client.post("/api/requests", json=payload), 201)

    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
