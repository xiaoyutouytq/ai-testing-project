
import requests


# 完整用户业务流程测试
def test_user_full_flow(base_url):
    username = "pytest_flow_user"
    old_password = "123456"
    new_password = "new123456"

    # 1. 注册用户
    register_response = requests.post(
        f"{base_url}/register",
        json={
            "username": username,
            "password": old_password
        }
    )

    assert register_response.status_code == 201
    assert register_response.json()["message"] == "注册成功"

    try:
        # 2. 使用原密码登录
        login_response = requests.post(
            f"{base_url}/login",
            json={
                "username": username,
                "password": old_password
            }
        )

        assert login_response.status_code == 200
        assert login_response.json()["token"]

        # 3. 修改密码
        update_response = requests.put(
            f"{base_url}/users/{username}",
            json={
                "password": new_password
            }
        )

        assert update_response.status_code == 200
        assert update_response.json()["message"] == "密码修改成功"

        # 4. 使用旧密码登录，应该失败
        old_login_response = requests.post(
            f"{base_url}/login",
            json={
                "username": username,
                "password": old_password
            }
        )

        assert old_login_response.status_code == 401

        # 5. 使用新密码登录，应该成功
        new_login_response = requests.post(
            f"{base_url}/login",
            json={
                "username": username,
                "password": new_password
            }
        )

        assert new_login_response.status_code == 200

        # 6. 删除用户
        delete_response = requests.delete(
            f"{base_url}/users/{username}"
        )

        assert delete_response.status_code == 200

        # 7. 删除后再次登录，应该失败
        deleted_login_response = requests.post(
            f"{base_url}/login",
            json={
                "username": username,
                "password": new_password
            }
        )

        assert deleted_login_response.status_code == 401

    finally:
        # 无论测试是否成功，都清理测试用户
        requests.delete(f"{base_url}/users/{username}")
