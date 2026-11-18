
import pytest
import requests

from test_data import NORMAL_MESSAGES, INVALID_MESSAGES, BOUNDARY_MESSAGES


# 公共函数：发送聊天请求
def send_chat(base_url, message=None, data=None):
    url = f"{base_url}/chat"

    if data is not None:
        return requests.post(url, json=data)

    return requests.post(url, json={"message": message})


# 1. 正常功能测试
def test_chat_success(base_url):
    response = send_chat(base_url, "你好")

    assert response.status_code == 200, "正常消息应该返回 HTTP 200"

    result = response.json()

    assert result["code"] == 200
    assert "answer" in result
    assert result["answer"]


# 2. 多问题参数化测试
@pytest.mark.parametrize("message", NORMAL_MESSAGES)
def test_chat_multiple_messages(base_url, message):
    response = send_chat(base_url, message)

    assert response.status_code == 200
    result = response.json()

    assert result["code"] == 200
    assert result["answer"]


# 3. 异常输入测试
@pytest.mark.parametrize("message", INVALID_MESSAGES)
def test_chat_invalid_message(base_url, message):
    response = send_chat(base_url, message)

    assert response.status_code == 400
    result = response.json()

    assert result["code"] == 400
    assert "error" in result


# 4. 缺少字段测试
def test_chat_missing_message(base_url):
    response = send_chat(base_url, data={})

    assert response.status_code == 400
    result = response.json()

    assert result["code"] == 400
    assert "error" in result


# 5. AI 输出格式检查
def test_chat_response_format(base_url):
    response = send_chat(base_url, "你好")

    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, dict)
    assert "code" in result
    assert "answer" in result
    assert isinstance(result["answer"], str)


# 6. 自定义错误信息
def test_chat_custom_error_message(base_url):
    response = send_chat(base_url, "")

    assert response.status_code == 400, "空消息应该被拒绝"

    result = response.json()

    assert result["error"] == "消息不能为空", "错误提示不正确"


# 7. 边界值测试
@pytest.mark.parametrize("message", BOUNDARY_MESSAGES)
def test_chat_boundary(base_url, message):
    response = send_chat(base_url, message)

    assert response.status_code == 200
    result = response.json()

    assert result["code"] == 200
    assert result["answer"]
