
import pytest
import requests


@pytest.mark.parametrize(
    "data, expected_status",
    [
        (None, 400),  # 不传请求数据
        ({}, 400),  # 空 JSON
        ({"username": "", "password": "123456"}, 400),
        ({"username": "tester", "password": ""}, 400),
        ({"username": 123, "password": "123456"}, 400),
        ({"username": "tester", "password": 123456}, 400),
    ]
)
def test_register_abnormal(base_url, data, expected_status):
    if data is None:
        response = requests.post(
            f"{base_url}/register"
        )
    else:
        response = requests.post(
            f"{base_url}/register",
            json=data
        )

    assert response.status_code == expected_status


# 测试重复注册
def test_register_duplicate(base_url):
    username = "pytest_duplicate_user"

    # 先清理可能残留的数据
    requests.delete(f"{base_url}/users/{username}")

    try:
        data = {
            "username": username,
            "password": "123456"
        }

        first_response = requests.post(
            f"{base_url}/register",
            json=data
        )

        assert first_response.status_code == 201

        second_response = requests.post(
            f"{base_url}/register",
            json=data
        )

        assert second_response.status_code == 409

    finally:
        requests.delete(f"{base_url}/users/{username}")
