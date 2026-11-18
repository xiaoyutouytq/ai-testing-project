
import os
import sqlite3
import logging
from pathlib import Path

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError

# 读取项目根目录的 .env
load_dotenv(Path(__file__).resolve().parent / ".env")

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "users.db")
VALID_TOKEN = "test_token_123"

# AI 模式：mock 不花钱，real 调用真实 DeepSeek
AI_MODE = os.getenv("AI_MODE", "mock").lower()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 保存不同会话的聊天记录
chat_sessions = {}


def get_ai_client():
    """创建 DeepSeek 客户端"""
    if not DEEPSEEK_API_KEY:
        raise ValueError("未配置 DEEPSEEK_API_KEY")

    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        timeout=30.0,
        max_retries=0
    )


def init_db():
    connection = sqlite3.connect(DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    connection.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "123456")
    )
    connection.commit()
    connection.close()


def get_db():
    return sqlite3.connect(DATABASE)


def mock_answer(message, history):
    """模拟 AI 回复，供免费自动化测试使用"""
    if "我叫什么" in message or "我的名字是什么" in message:
        for old_message in reversed(history):
            if old_message["role"] == "user":
                old_text = old_message["content"]
                if old_text.startswith("我叫"):
                    return f"AI回复：你叫{old_text[2:].strip()}。"

        return "AI回复：我还不知道你的名字。"

    return f"AI回复：你刚才说的是：{message}"


def get_ai_answer(message, history):
    """调用真实 DeepSeek API"""
    client = get_ai_client()

    messages = [
        {
            "role": "system",
            "content": "你是一个友好、乐于助人的中文AI助手。"
        }
    ]

    # 只发送最近20条历史消息，控制请求长度
    messages.extend(history[-20:])
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        max_tokens=300,
        extra_body={
            "thinking": {"type": "disabled"}
        }
    )

    answer = response.choices[0].message.content

    if not answer or not answer.strip():
        raise ValueError("AI 返回了空回复")

    return answer.strip()


@app.route("/chat", methods=["POST"])
def chat():
    # 校验 Token
    auth_header = request.headers.get("Authorization", "")

    if auth_header != "Bearer test_token_123":
        return jsonify({
            "error": "Unauthorized",
            "message": "无效的 Token"
        }), 401
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"code": 400, "error": "请求数据格式错误"}), 400

    message = data.get("message")
    session_id = data.get("session_id")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"code": 400, "error": "消息不能为空"}), 400

    message = message.strip()

    if session_id is not None:
        if not isinstance(session_id, str) or not session_id.strip():
            return jsonify({"code": 400, "error": "session_id 格式错误"}), 400

        session_id = session_id.strip()
        history = chat_sessions.setdefault(session_id, [])
    else:
        # 不带 session_id 时，不保存历史记录
        history = []

    try:
        if AI_MODE == "real":
            answer = get_ai_answer(message, history)
        else:
            answer = mock_answer(message, history)

    except APITimeoutError:
        logger.warning("DeepSeek API 请求超时")
        return jsonify({
            "code": 504,
            "error": "AI 服务请求超时"
        }), 504

    except ValueError as error:
        logger.error("AI 配置或回复异常：%s", error)
        return jsonify({
            "code": 500,
            "error": "AI 服务配置错误或返回异常"
        }), 500

    except APIError as error:
        logger.error("DeepSeek API 调用失败：%s", error.status_code)
        return jsonify({
            "code": 502,
            "error": "AI 服务调用失败",
            "upstream_status": error.status_code
        }), 502

    except Exception:
        logger.exception("AI 服务发生未知异常")
        return jsonify({
            "code": 500,
            "error": "服务器内部错误"
        }), 500

    # 只有成功得到回复后，才保存对话
    if session_id is not None:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": answer})

    result = {
        "code": 200,
        "answer": answer
    }

    if session_id is not None:
        result["session_id"] = session_id

    return jsonify(result), 200


@app.route("/chat/clear", methods=["POST"])
def clear_chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"code": 400, "error": "请求数据格式错误"}), 400

    session_id = data.get("session_id")

    if not isinstance(session_id, str) or not session_id.strip():
        return jsonify({"code": 400, "error": "session_id 不能为空"}), 400

    chat_sessions.pop(session_id.strip(), None)

    return jsonify({
        "code": 200,
        "message": "会话记录已清空"
    }), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"code": 400, "error": "请求数据格式错误"}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return jsonify({"code": 400, "error": "账号不能为空或格式错误"}), 400

    if not isinstance(password, str) or not password.strip():
        return jsonify({"code": 400, "error": "密码不能为空或格式错误"}), 400

    connection = get_db()

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        connection.commit()

        return jsonify({"code": 201, "message": "注册成功"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"code": 409, "error": "用户名已存在"}), 409

    finally:
        connection.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"code": 400, "error": "请求数据格式错误"}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return jsonify({"code": 400, "error": "账号不能为空或格式错误"}), 400

    if not isinstance(password, str) or not password.strip():
        return jsonify({"code": 400, "error": "密码不能为空或格式错误"}), 400

    connection = get_db()

    try:
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
    finally:
        connection.close()

    if user is None or user[2] != password:
        return jsonify({"code": 401, "error": "账号或密码错误"}), 401

    return jsonify({
        "code": 200,
        "message": "登录成功",
        "token": VALID_TOKEN
    }), 200


@app.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")

    if token != f"Bearer {VALID_TOKEN}":
        return jsonify({"code": 401, "error": "Token 无效或缺失"}), 401

    return jsonify({
        "code": 200,
        "username": "admin",
        "message": "身份验证成功"
    }), 200


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    connection = get_db()

    try:
        user = connection.execute(
            "SELECT username FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user is None:
            return jsonify({"code": 404, "error": "用户不存在"}), 404

        return jsonify({"code": 200, "username": user[0]}), 200

    finally:
        connection.close()


@app.route("/users/<username>", methods=["PUT"])
def update_user(username):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"code": 400, "error": "请求数据格式错误"}), 400

    new_password = data.get("password")

    if not isinstance(new_password, str) or not new_password.strip():
        return jsonify({"code": 400, "error": "新密码不能为空或格式错误"}), 400

    connection = get_db()

    try:
        cursor = connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password, username)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"code": 404, "error": "用户不存在"}), 404

        return jsonify({"code": 200, "message": "密码修改成功"}), 200

    finally:
        connection.close()


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    connection = get_db()

    try:
        cursor = connection.execute(
            "DELETE FROM users WHERE username = ?",
            (username,)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"code": 404, "error": "用户不存在"}), 404

        return jsonify({"code": 200, "message": "用户删除成功"}), 200

    finally:
        connection.close()


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
