
import sqlite3
import pytest
import requests

from app import DATABASE


# 每个测试前后清理测试用户
@pytest.fixture
def test_username():
    username = "pytest_user_001"

    connection = sqlite3.connect(DATABASE)
    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )
    connection.commit()
    connection.close()

    yield username

    connection = sqlite3.connect(DATABASE)
    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )
    connection.commit()
    connection.close()


# 1. 测试注册成功，并验证数据库确实有记录
def test_register_success(base_url, test_username):
    response = requests.post(
        f"{base_url}/register",
        json={
            "username": test_username,
            "password": "123456"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "注册成功"

    # 查询数据库，确认数据已经写入
    connection = sqlite3.connect(DATABASE)

    result = connection.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (test_username,)
    ).fetchone()

    connection.close()

    assert result is not None
    assert result[0] == test_username
    assert result[1] == "123456"


# 2. 测试重复注册
def test_register_duplicate(base_url, test_username):
    data = {
        "username": test_username,
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
    assert second_response.json()["error"] == "用户名已存在"


# 3. 测试缺少注册信息
def test_register_missing_data(base_url):
    response = requests.post(
        f"{base_url}/register",
        json={
            "username": "pytest_user_002"
        }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "密码不能为空或格式错误"
