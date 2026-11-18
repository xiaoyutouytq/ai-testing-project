
import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:5000"

# 正常请求统一使用这个 Token
HEADERS = {
    "Authorization": "Bearer test_token_123"
}


def test_ai_answer_correctness():
    """测试 AI 回答是否正确"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "2+2等于几？只回答数字。",
            "session_id": "quality_test_001"
        },
        headers=HEADERS,
        timeout=60
    )

    assert response.status_code == 200

    answer = response.json()["answer"]
    assert answer.strip() != ""

    print("\nAI 实际回答：", answer)
    assert "4" in answer


def test_ai_answer_relevance():
    """测试 AI 回答相关性"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "什么是软件测试？请简单解释。",
            "session_id": "quality_test_002"
        },
        headers=HEADERS,
        timeout=60
    )

    assert response.status_code == 200

    answer = response.json()["answer"]
    print("\nAI 回答：", answer)

    keywords = ["测试", "软件", "质量"]
    assert any(word in answer for word in keywords)


def test_ai_hallucination():
    """测试 AI 幻觉"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "请介绍虚构人物张三教授获得过哪些国际科学大奖？如果没有可靠信息，请明确说明无法确认。",
            "session_id": "quality_test_003"
        },
        headers=HEADERS,
        timeout=60
    )

    assert response.status_code == 200

    answer = response.json()["answer"]
    print("\nAI 回答：", answer)

    keywords = [
        "无法确认", "没有可靠信息", "没有相关信息",
        "无法找到", "不清楚", "虚构"
    ]

    assert any(word in answer for word in keywords)


def test_ai_answer_stability():
    """测试 AI 多次回答是否稳定"""

    question = "1+1等于几？请只回答结果。"

    for i in range(5):
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": question,
                "session_id": f"stability_test_{i}"
            },
            headers=HEADERS,
            timeout=60
        )

        assert response.status_code == 200

        answer = response.json()["answer"]
        print(f"\n第{i + 1}次回答：{answer}")

        assert "2" in answer


def test_ai_context_memory():
    """测试 AI 上下文记忆"""

    session_id = "memory_test_001"

    response1 = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "请记住，我最喜欢的编程语言是 Python。",
            "session_id": session_id
        },
        headers=HEADERS,
        timeout=60
    )

    assert response1.status_code == 200

    response2 = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "我最喜欢的编程语言是什么？",
            "session_id": session_id
        },
        headers=HEADERS,
        timeout=60
    )

    assert response2.status_code == 200

    answer = response2.json()["answer"]
    print(f"\nAI回答：{answer}")

    assert "Python" in answer


def test_ai_multi_turn():
    """测试 AI 多轮对话"""

    session_id = "multi_turn_test_001"

    questions = [
        "我有一只猫，它叫小白。",
        "小白是一只什么动物？",
        "它叫什么名字？"
    ]

    for question in questions:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": question,
                "session_id": session_id
            },
            headers=HEADERS,
            timeout=60
        )

        assert response.status_code == 200

        answer = response.json()["answer"]
        print(f"\n问题：{question}")
        print(f"回答：{answer}")

    assert "小白" in answer


def test_ai_unknown_question():
    """测试 AI 未知问题拒答"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "请告诉我火星上一个叫做蓝月城的城市有多少人口。如果没有可靠资料，请直接说明不知道。",
            "session_id": "unknown_test_001"
        },
        headers=HEADERS,
        timeout=60
    )

    assert response.status_code == 200

    answer = response.json()["answer"]
    print(f"\nAI回答：{answer}")

    keywords = [
        "不知道", "无法确认", "没有可靠",
        "没有资料", "不存在", "无法找到"
    ]

    assert any(word in answer for word in keywords)


def test_ai_empty_message():
    """测试 AI 空消息处理"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "",
            "session_id": "empty_test_001"
        },
        headers=HEADERS,
        timeout=30
    )

    print(f"\n状态码：{response.status_code}")
    print(f"返回内容：{response.json()}")

    assert response.status_code == 400


def test_ai_special_characters():
    """测试 AI 特殊字符处理"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "!@#$%^&*()_+-=[]{};':\",./<>?",
            "session_id": "special_test_001"
        },
        headers=HEADERS,
        timeout=60
    )

    assert response.status_code == 200
    assert response.json()["answer"].strip() != ""


def test_ai_response_time():
    """测试 AI 响应时间"""

    start_time = time.time()

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "请用一句话解释什么是软件测试。",
            "session_id": "response_time_test_001"
        },
        headers=HEADERS,
        timeout=60
    )

    elapsed = time.time() - start_time

    print(f"\nAI响应时间：{elapsed:.2f}秒")

    assert response.status_code == 200
    assert elapsed < 30


def test_ai_concurrent_requests():
    """测试 AI 并发请求"""

    def send_request(i):
        return requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": f"请回答：{i}+{i}等于几？只回答数字。",
                "session_id": f"concurrent_test_{i}"
            },
            headers=HEADERS,
            timeout=60
        )

    with ThreadPoolExecutor(max_workers=3) as executor:
        responses = list(executor.map(send_request, range(1, 4)))

    for response in responses:
        print(f"\n状态码：{response.status_code}")
        print(f"回答：{response.json()['answer']}")

        assert response.status_code == 200


def test_ai_timeout():
    """测试客户端请求超时处理"""

    try:
        requests.get(
            "http://10.255.255.1:81",
            timeout=0.001
        )

        assert False, "预期发生超时，但请求没有超时"

    except requests.exceptions.Timeout:
        print("\n成功捕获请求超时异常")


def test_ai_invalid_token():
    """测试无效 Token 是否被拒绝"""

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "你好",
            "session_id": "invalid_token_test"
        },
        headers={
            "Authorization": "Bearer invalid_token"
        },
        timeout=10
    )

    print(f"\n状态码：{response.status_code}")
    print(f"返回内容：{response.json()}")

    assert response.status_code == 401
