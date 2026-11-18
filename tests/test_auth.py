
import requests


# 1. 登录成功
def test_login_success(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    result = response.json()

    assert result["code"] == 200
    assert result["token"]


# 2. 错误密码
def test_login_wrong_password(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "wrong123"
        }
    )

    assert response.status_code == 401
    assert response.json()["code"] == 401


# 3. 错误账号
def test_login_wrong_username(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "wrong",
            "password": "123456"
        }
    )

    assert response.status_code == 401


# 4. 缺少账号
def test_login_missing_username(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "password": "123456"
        }
    )

    assert response.status_code == 400


# 5. 缺少密码
def test_login_missing_password(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin"
        }
    )

    assert response.status_code == 400


# 6. 没有 Token
def test_profile_without_token(base_url):
    response = requests.get(
        f"{base_url}/profile"
    )

    assert response.status_code == 401


# 7. 正确 Token：自动从 fixture 获取
def test_profile_with_token(base_url, auth_headers):
    response = requests.get(
        f"{base_url}/profile",
        headers=auth_headers
    )

    assert response.status_code == 200
    result = response.json()

    assert result["code"] == 200
    assert result["username"] == "admin"


# 8. 再次使用同一个 Token
def test_profile_with_token_again(base_url, auth_headers):
    response = requests.get(
        f"{base_url}/profile",
        headers=auth_headers
    )

    assert response.status_code == 200
    result = response.json()

    assert result["code"] == 200
    assert result["username"] == "admin"


# 9. 错误 Token
def test_profile_with_wrong_token(base_url):
    response = requests.get(
        f"{base_url}/profile",
        headers={
            "Authorization": "Bearer wrong_token"
        }
    )

    assert response.status_code == 401
