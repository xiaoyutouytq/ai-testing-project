
import pytest


@pytest.fixture
def test_user():
    # 测试前：准备数据
    print("\n测试前：创建测试用户")

    user = {
        "username": "test001",
        "password": "123456"
    }

    # 把数据交给测试函数
    yield user

    # 测试后：清理数据
    print("\n测试后：删除测试用户")


def test_user_username(test_user):
    print("正在测试用户名")

    assert test_user["username"] == "test001"


def test_user_password(test_user):
    print("正在测试密码")

    assert test_user["password"] == "123456"
