
import sqlite3
import pytest


# 创建数据库连接和测试表
@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    yield connection

    connection.close()


# 测试插入数据
def test_insert_user(db):
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "123456")
    )

    db.commit()

    result = db.execute(
        "SELECT username FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    assert result[0] == "admin"


# 测试查询数据
def test_query_user(db):
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("tester001", "123456")
    )

    db.commit()

    result = db.execute(
        "SELECT * FROM users WHERE username = ?",
        ("tester001",)
    ).fetchone()

    assert result is not None
    assert result[1] == "tester001"


# 测试数据是否不存在
def test_user_not_exist(db):
    result = db.execute(
        "SELECT * FROM users WHERE username = ?",
        ("unknown",)
    ).fetchone()

    assert result is None
