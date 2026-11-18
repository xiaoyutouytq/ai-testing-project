import pytest
import requests


@pytest.mark.parametrize(
    "data, expected_status",
    [
        (None, 400),
        ({}, 400),
        ({"password": "123456"}, 400),
        ({"username": "admin"}, 400),
        ({"username": "", "password": "123456"}, 400),
        ({"username": "admin", "password": ""}, 400),
        ({"username": 123, "password": "123456"}, 400),
        ({"username": "admin", "password": 123456}, 400),
        ({"username": "wrong_user", "password": "123456"}, 401),
        ({"username": "admin", "password": "wrong_password"}, 401),
    ]
)
def test_login_abnormal(base_url, data, expected_status):
    if data is None:
        response = requests.post(f"{base_url}/login")
    else:
        response = requests.post(
            f"{base_url}/login",
            json=data
        )

    assert response.status_code == expected_status