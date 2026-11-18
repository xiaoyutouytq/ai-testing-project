
import sqlite3
import pytest
import requests

from app import DATABASE


@pytest.fixture
def test_user():
    username = "pytest_manage_user"
    password = "123456"

    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )

    connection.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
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


# 测试修改密码
def test_update_password(base_url, test_user):
    response = requests.put(
        f"{base_url}/users/{test_user}",
        json={"password": "new123456"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "密码修改成功"

    # 查询数据库，确认密码确实修改了
    connection = sqlite3.connect(DATABASE)

    result = connection.execute(
        "SELECT password FROM users WHERE username = ?",
        (test_user,)
    ).fetchone()

    connection.close()

    assert result[0] == "new123456"


# 测试修改不存在的用户
def test_update_missing_user(base_url):
    response = requests.put(
        f"{base_url}/users/not_exist_user",
        json={"password": "new123456"}
    )

    assert response.status_code == 404


# 测试新密码为空
def test_update_empty_password(base_url, test_user):
    response = requests.put(
        f"{base_url}/users/{test_user}",
        json={"password": ""}
    )

    assert response.status_code == 400


# 测试删除用户
def test_delete_user(base_url, test_user):
    response = requests.delete(
        f"{base_url}/users/{test_user}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "用户删除成功"

    # 查询数据库，确认用户已经删除
    connection = sqlite3.connect(DATABASE)

    result = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (test_user,)
    ).fetchone()

    connection.close()

    assert result is None


# 测试删除不存在的用户
def test_delete_missing_user(base_url):
    response = requests.delete(
        f"{base_url}/users/not_exist_user"
    )

    assert response.status_code == 404
