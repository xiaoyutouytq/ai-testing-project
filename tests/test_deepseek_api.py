
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from openai import OpenAI


# 从项目根目录读取 .env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("DEEPSEEK_API_KEY")


def test_deepseek_api():
    # 检查 API Key 是否配置
    assert API_KEY, "没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件"

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己。"}
        ],
        max_tokens=100,
        extra_body={
            "thinking": {"type": "disabled"}
        }
    )

    answer = response.choices[0].message.content

    print("\nDeepSeek 回复：", answer)

    assert answer is not None
    assert len(answer.strip()) > 0
