import pytest
import requests


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"message": ""},
        {"message": "   "},
        {"message": 123},
        {"message": None},
        {"message": []},
        {"message": {}},
    ]
)
def test_chat_abnormal(base_url, data):
    response = requests.post(
        f"{base_url}/chat",
        json=data
    )

    assert response.status_code == 400

    result = response.json()

    assert result["code"] == 400
    assert result["error"] == "消息不能为空"


def test_chat_special_characters(base_url):
    response = requests.post(
        f"{base_url}/chat",
        json={"message": "!@#$%^&*()中文测试"}
    )

    assert response.status_code == 200

    result = response.json()

    assert "!@#$%^&*()中文测试" in result["answer"]


def test_chat_long_message(base_url):
    message = "测试" * 10000

    response = requests.post(
        f"{base_url}/chat",
        json={"message": message}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["answer"] == f"AI回复：你刚才说的是：{message}"