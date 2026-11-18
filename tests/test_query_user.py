
import sqlite3
import pytest
import requests

from app import DATABASE


@pytest.fixture
def test_user():
    username = "pytest_query_user"

    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )

    connection.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, "123456")
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


# 1. 查询存在的用户
def test_query_user_success(base_url, test_user):
    response = requests.get(
        f"{base_url}/users/{test_user}"
    )

    assert response.status_code == 200
    assert response.json()["username"] == test_user


# 2. 查询不存在的用户
def test_query_user_not_exist(base_url):
    response = requests.get(
        f"{base_url}/users/not_exist_user"
    )

    assert response.status_code == 404
    assert response.json()["error"] == "用户不存在"


# 3. 查询后验证数据库记录
def test_query_user_database(base_url, test_user):
    response = requests.get(
        f"{base_url}/users/{test_user}"
    )

    assert response.status_code == 200

    connection = sqlite3.connect(DATABASE)

    result = connection.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (test_user,)
    ).fetchone()

    connection.close()

    assert result is not None
    assert result[0] == test_user
    assert result[1] == "123456"
