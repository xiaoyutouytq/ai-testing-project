import requests


def test_chat_user_isolation(base_url):
    user_a_message = "我叫小明"
    user_b_message = "我叫小红"

    # 用户 A 发送消息
    response_a = requests.post(
        f"{base_url}/chat",
        json={"message": user_a_message}
    )

    assert response_a.status_code == 200

    answer_a = response_a.json()["answer"]

    # 用户 B 发送消息
    response_b = requests.post(
        f"{base_url}/chat",
        json={"message": user_b_message}
    )

    assert response_b.status_code == 200

    answer_b = response_b.json()["answer"]

    # 验证两条消息没有混淆
    assert user_a_message in answer_a
    assert user_b_message in answer_b

    assert user_b_message not in answer_a
    assert user_a_message not in answer_b