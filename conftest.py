
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


# 整个测试过程共享 base_url
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


# 整个测试过程只登录一次
@pytest.fixture(scope="session")
def auth_token(base_url):
    print("\n正在登录，获取 Token...")

    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "123456"
        }
    )

    assert response.status_code == 200, "登录失败"

    token = response.json()["token"]

    print("Token 获取成功")

    return token


# 整个测试过程共享请求头
@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }
