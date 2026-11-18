import pytest
import requests


@pytest.mark.parametrize(
    "data, expected_status",
    [
        (None, 400),
        ({}, 400),
        ({"password": ""}, 400),
        ({"password": 123456}, 400),
    ]
)
def test_update_user_abnormal(base_url, data, expected_status):
    if data is None:
        response = requests.put(
            f"{base_url}/users/admin"
        )
    else:
        response = requests.put(
            f"{base_url}/users/admin",
            json=data
        )

    assert response.status_code == expected_status


def test_update_nonexistent_user(base_url):
    response = requests.put(
        f"{base_url}/users/not_exist_user_001",
        json={"password": "new123456"}
    )

    assert response.status_code == 404