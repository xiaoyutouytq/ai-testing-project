
import requests


def test_chat_clear_memory(base_url):
    session_id = "clear_memory_test"

    # 先清空历史记录
    requests.post(
        f"{base_url}/chat/clear",
        json={"session_id": session_id}
    )

    # 告诉 AI 自己的名字
    requests.post(
        f"{base_url}/chat",
        json={
            "session_id": session_id,
            "message": "我叫小明"
        }
    )

    # 清空会话记忆
    clear_response = requests.post(
        f"{base_url}/chat/clear",
        json={"session_id": session_id}
    )

    assert clear_response.status_code == 200

    # 再次询问自己的名字
    response = requests.post(
        f"{base_url}/chat",
        json={
            "session_id": session_id,
            "message": "我叫什么？"
        }
    )

    assert response.status_code == 200

    answer = response.json()["answer"]

    assert "小明" not in answer
    assert "还不知道你的名字" in answer

    # 清理测试数据
    requests.post(
        f"{base_url}/chat/clear",
        json={"session_id": session_id}
    )
