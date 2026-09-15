import pytest

from tests.utils.assertions import assert_error, assert_fields, assert_json_response

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_get_current_profile(authenticated_client, registered_user):
    body = assert_json_response(authenticated_client.get("/api/users/me"), 200)

    assert_fields(body, ["id", "email", "full_name", "department"])
    assert body["email"] == registered_user["email"]
    assert body["full_name"] == registered_user["full_name"]


def test_update_profile_changes_allowed_fields(authenticated_client):
    body = assert_json_response(
        authenticated_client.put(
            "/api/users/me",
            json={"full_name": "Updated QA Engineer", "department": "Platform Quality"},
        ),
        200,
    )

    assert body["full_name"] == "Updated QA Engineer"
    assert body["department"] == "Platform Quality"


def test_profile_update_persists(authenticated_client):
    authenticated_client.put(
        "/api/users/me",
        json={"full_name": "Persistent Profile", "department": "Regression"},
    )

    body = assert_json_response(authenticated_client.get("/api/users/me"), 200)
    assert body["full_name"] == "Persistent Profile"
    assert body["department"] == "Regression"


def test_profile_missing_authentication_is_rejected(api_client):
    assert_error(
        api_client.put("/api/users/me", json={"full_name": "No Auth"}),
        401,
        "authentication required",
    )


@pytest.mark.parametrize(
    "payload, field",
    [
        ({"full_name": "A"}, "full_name"),
        ({"department": "A"}, "department"),
        ({"full_name": 42}, "full_name"),
    ],
)
def test_invalid_profile_data_returns_validation_error(authenticated_client, payload, field):
    body = assert_error(authenticated_client.put("/api/users/me", json=payload), 422)

    assert field in str(body["detail"])


def test_profile_accepts_boundary_length_values(authenticated_client):
    max_name = "A" * 120
    max_department = "Q" * 80

    body = assert_json_response(
        authenticated_client.put(
            "/api/users/me",
            json={"full_name": max_name, "department": max_department},
        ),
        200,
    )

    assert body["full_name"] == max_name
    assert body["department"] == max_department
