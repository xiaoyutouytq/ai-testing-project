import requests


def test_delete_nonexistent_user(base_url):
    response = requests.delete(
        f"{base_url}/users/not_exist_user_002"
    )

    assert response.status_code == 404


def test_delete_same_user_twice(base_url):
    username = "pytest_delete_twice"

    # 先清理历史数据
    requests.delete(f"{base_url}/users/{username}")

    try:
        # 第一次注册
        register_response = requests.post(
            f"{base_url}/register",
            json={
                "username": username,
                "password": "123456"
            }
        )

        assert register_response.status_code == 201

        # 第一次删除
        first_response = requests.delete(
            f"{base_url}/users/{username}"
        )

        assert first_response.status_code == 200

        # 第二次删除
        second_response = requests.delete(
            f"{base_url}/users/{username}"
        )

        assert second_response.status_code == 404

    finally:
        requests.delete(f"{base_url}/users/{username}")