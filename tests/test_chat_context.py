
import requests


def test_chat_context_isolation(base_url):
    session_a = "user_a_context"
    session_b = "user_b_context"

    # 清理两个会话
    for session_id in [session_a, session_b]:
        requests.post(
            f"{base_url}/chat/clear",
            json={"session_id": session_id}
        )

    try:
        # 用户 A 告诉 AI 自己的名字
        requests.post(
            f"{base_url}/chat",
            json={
                "session_id": session_a,
                "message": "我叫小明"
            }
        )

        # 用户 B 询问自己的名字
        response = requests.post(
            f"{base_url}/chat",
            json={
                "session_id": session_b,
                "message": "我叫什么？"
            }
        )

        assert response.status_code == 200

        answer = response.json()["answer"]

        # 用户 B 不应该知道用户 A 的名字
        assert "小明" not in answer
        assert "还不知道你的名字" in answer

    finally:
        requests.post(
            f"{base_url}/chat/clear",
            json={"session_id": session_a}
        )
        requests.post(
            f"{base_url}/chat/clear",
            json={"session_id": session_b}
        )
