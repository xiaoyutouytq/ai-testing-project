import pytest
import requests


@pytest.mark.parametrize(
    "username, expected_status",
    [
        ("not_exist_user_001", 404),
        ("not_exist_user_002", 404),
    ]
)
def test_query_nonexistent_user(base_url, username, expected_status):
    response = requests.get(
        f"{base_url}/users/{username}"
    )

    assert response.status_code == expected_status


def test_query_user_response_format(base_url):
    response = requests.get(
        f"{base_url}/users/admin"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == 200
    assert data["username"] == "admin"