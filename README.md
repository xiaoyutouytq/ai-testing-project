# AI 应用自动化测试项目

## 一、项目介绍

本项目是一个基于 Python、Flask、pytest 和 DeepSeek API 搭建的 AI 应用自动化测试项目。

通过自动化测试验证 AI 聊天接口的功能、回答质量、异常处理、安全性和基础性能。

## 二、技术栈

- Python
- Flask
- pytest
- requests
- DeepSeek API
- SQLite
- pytest-html
- Git

## 三、项目功能

1. AI 聊天接口
2. AI 多轮对话
3. Session 会话记忆
4. 对话历史管理
5. Token 身份验证
6. AI 模拟模式与真实 API 模式

## 四、自动化测试内容

目前已完成 13 项测试：

| 测试类型 | 测试内容 |
|---|---|
| 功能测试 | AI 回答正确性 |
| 质量测试 | 回答相关性 |
| 质量测试 | 幻觉初步筛查 |
| 稳定性测试 | 多次回答稳定性 |
| 上下文测试 | 上下文记忆 |
| 对话测试 | 多轮对话 |
| 质量测试 | 未知问题拒答 |
| 异常测试 | 空消息 |
| 异常测试 | 特殊字符 |
| 性能测试 | 响应时间 |
| 并发测试 | 3个并发请求 |
| 异常测试 | 请求超时 |
| 安全测试 | 无效 Token |

## 五、项目运行

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=填写自己的API_KEY
AI_MODE=real
DEEPSEEK_MODEL=deepseek-flash
```

注意：不要将真实 API Key 上传到 GitHub。

### 3. 启动 Flask

```bash
python app.py
```

### 4. 执行自动化测试

```bash
pytest -v -s tests/test_ai_quality.py
```

### 5. 生成 HTML 测试报告

```bash
pytest -v tests/test_ai_quality.py --html=reports/ai_test_report.html --self-contained-html
```

## 六、测试结果

第一轮 AI 质量测试：

- 自动化测试用例：13项
- 通过数量：13项
- 失败数量：0项

测试通过率：100%

## 七、项目收获

- 掌握 Python 接口自动化测试
- 掌握 pytest 测试框架
- 掌握 requests 接口请求
- 掌握 AI 应用质量测试
- 掌握 AI 多轮对话测试
- 掌握基础并发测试
- 掌握 Token 鉴权测试
- 掌握 pytest-html 测试报告生成
