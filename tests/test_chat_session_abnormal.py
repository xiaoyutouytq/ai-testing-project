
import pytest
import requests


@pytest.mark.parametrize(
    "session_id",
    [
        "",
        "   ",
        123,
        [],
        {},
    ]
)
def test_chat_invalid_session_id(base_url, session_id):
    response = requests.post(
        f"{base_url}/chat",
        json={
            "session_id": session_id,
            "message": "你好"
        }
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"session_id": ""},
        {"session_id": "   "},
        {"session_id": 123},
        {"session_id": []},
        {"session_id": {}},
    ]
)
def test_clear_invalid_session_id(base_url, data):
    response = requests.post(
        f"{base_url}/chat/clear",
        json=data
    )

    assert response.status_code == 400
