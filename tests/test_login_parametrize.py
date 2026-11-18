
import pytest
import requests


@pytest.mark.parametrize(
    "username,password,expected_status",
    [
        ("admin", "123456", 200),          # 正确账号和密码
        ("admin", "wrong123", 401),        # 密码错误
        ("wrong_user", "123456", 401),     # 账号不存在
        ("", "123456", 400),               # 账号为空
        ("admin", "", 400),                # 密码为空
    ]
)
def test_login_cases(base_url, username, password, expected_status):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == expected_status
