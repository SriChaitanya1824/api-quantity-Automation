import pytest

from tests.utils.assertions import assert_error, assert_fields, assert_json_response
from tests.utils.data_generator import valid_user

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_register_user_success(api_client):
    payload = valid_user()
    body = assert_json_response(api_client.post("/api/auth/register", json=payload), 201)

    assert_fields(body, ["id", "email", "full_name", "department"])
    assert body["email"] == payload["email"]
    assert "password" not in body
    assert "password_hash" not in body


def test_duplicate_registration_returns_conflict(api_client):
    payload = valid_user()
    assert api_client.post("/api/auth/register", json=payload).status_code == 201

    assert_error(api_client.post("/api/auth/register", json=payload), 409, "already registered")


@pytest.mark.parametrize(
    "payload, expected_fragment",
    [
        ({"email": "missing-name@example.test", "password": "Password123!"}, "full_name"),
        ({"email": "not-an-email", "password": "Password123!", "full_name": "Bad Email"}, "email"),
        (
            {
                "email": "short-password@example.test",
                "password": "short",
                "full_name": "Short Password",
            },
            "password",
        ),
    ],
)
def test_invalid_registration_payloads_return_validation_errors(
    api_client, payload, expected_fragment
):
    body = assert_error(api_client.post("/api/auth/register", json=payload), 422)

    assert expected_fragment in str(body["detail"])


@pytest.mark.smoke
def test_login_success_returns_bearer_token(api_client, registered_user):
    response = api_client.post(
        "/api/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    body = assert_json_response(response, 200)

    assert_fields(body, ["access_token", "token_type"])
    assert body["token_type"] == "bearer"
    assert len(body["access_token"].split(".")) == 3


def test_login_with_incorrect_password_is_rejected(api_client, registered_user):
    assert_error(
        api_client.post(
            "/api/auth/login",
            json={"email": registered_user["email"], "password": "WrongPassword123!"},
        ),
        401,
        "invalid email or password",
    )


def test_login_with_unknown_user_is_rejected(api_client):
    assert_error(
        api_client.post(
            "/api/auth/login",
            json={"email": "unknown@brivo-qa.example.com", "password": "Password123!"},
        ),
        401,
        "invalid email or password",
    )


def test_login_missing_credentials_returns_validation_error(api_client):
    body = assert_error(
        api_client.post("/api/auth/login", json={"email": "missing@brivo-qa.example.com"}), 422
    )

    assert "password" in str(body["detail"])


def test_invalid_jwt_is_rejected(api_client):
    client = api_client.authenticated("not-a-valid-jwt")

    assert_error(client.get("/api/users/me"), 401, "invalid authentication token")


def test_protected_endpoint_requires_authentication(api_client):
    assert_error(api_client.get("/api/users/me"), 401, "authentication required")
