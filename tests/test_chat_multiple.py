import requests


def test_chat_multiple_messages(base_url):
    messages = [
        "你好",
        "什么是软件测试？",
        "什么是自动化测试？",
        "pytest有什么作用？"
    ]

    for message in messages:
        response = requests.post(
            f"{base_url}/chat",
            json={"message": message}
        )

        assert response.status_code == 200

        result = response.json()

        assert result["code"] == 200
        assert result["answer"] == f"AI回复：你刚才说的是：{message}"