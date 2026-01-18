# WebGPT - ChatGPT Web to API Gateway

WebGPT 是一个将 ChatGPT 网页版 (`chatgpt.com`) 转化为标准 OpenAI API 格式的网关服务。它允许你使用任意支持 OpenAI 接口的客户端（如 Chatbox, LangChain, AutoGen 等）来调用 ChatGPT 网页版的免费或 Plus 账号能力，包括且不限于 GPT-4 模型和**多模态图片分析**。

---

## 🚀 核心特性

- **OpenAI 兼容接口**: 提供 `/v1/chat/completions` 端点。
- **多模态支持**: 支持发送本地图片路径进行视觉分析 (GPT-4 Vision)。
- **抗指纹检测**: 使用 CDP (Chrome DevTools Protocol) 接管现有 Chrome 浏览器，完美绕过 Cloudflare 验证。
- **自动日志**: 所有对话记录自动保存至 `chat_history.jsonl`。

---

## 🛠️ 项目结构与模块说明

项目位于 `d:\webgpt`，核心文件结构如下：

| 文件名 | 类型 | 功能说明 | 解决的问题 |
| :--- | :--- | :--- | :--- |
| **`main.py`** | 核心 | **API 网关入口 (FastAPI)**。<br>定义了 HTTP 接口，接收客户端请求，解析多模态消息格式，调用 `browser_manager` 执行操作，并记录日志。 | 统一接口规范，处理输入数据的校验与格式转换 (OpenAI 格式 -> 浏览器操作指令)。 |
| **`browser_manager.py`** | 核心 | **浏览器自动化控制器 (Playwright)**。<br>封装了所有与 Chrome 交互的逻辑：连接调试端口、查找输入框、上传文件、点击发送、监控生成状态、提取回答文本。 | 屏蔽网页自动化的复杂性（如 DOM 变化、等待逻辑、文件上传），提供稳定的 `send_message` 接口。 |
| **`start_chrome_debug.bat`** | 脚本 | **Chrome 调试启动器**。<br>启动一个开启了无需界面 (Headless) 或 远程调试端口 (9222) 的 Chrome 实例。 | **解决 Cloudflare 验证难题**。通过复用用户日常登录的浏览器环境，避免被识别为机器人路径。 |
| **`run_headless.bat`** | 脚本 | **服务启动脚本**。<br>启动 `main.py` 后台服务。 | 一键启动 API 服务，连接已打开的 Chrome。 |
| **`setup_login.bat`** | 脚本 | (可选) 首次登录辅助脚本。 | 帮助用户初始化环境（但在 CDP 模式下，直接用 `start_chrome_debug.bat` 登录即可）。 |
| **`requirements.txt`** | 依赖 | Python 依赖库列表 (FastAPI, Playwright, Uvicorn 等)。 | 确保运行环境一致性。 |
| **`chat_history.jsonl`** | 数据 | 自动生成的对话日志文件。 | 数据留存与回溯。 |

---

## 💻 部署与运行环境要求

### 硬件要求
- **操作系统**: Windows 10/11 (目前的脚本是 `.bat`，Linux/Mac 需改写启动脚本)。
- **内存**: 建议 4GB 以上 (Chrome 占用较大)。

### 软件要求
1.  **Python 3.8+**: 需添加到系统 PATH。
2.  **Google Chrome**: 必须安装标准版 Chrome 浏览器。
3.  **网络**: 能够访问 `chatgpt.com` 的网络环境。

### 部署步骤 (在另一台机器上)

1.  **拷贝文件**: 将整个 `webgpt` 文件夹复制到新机器。
2.  **安装依赖**:
    ```powershell
    cd webgpt
    pip install -r requirements.txt
    python -m playwright install chromium
    ```
3.  **配置 Chrome 路径**:
    - 如果你的 Chrome 安装在默认位置，无需修改。
    - 如果安装在非标位置，编辑 `start_chrome_debug.bat` 修改 `CHROME_PATH`。

---

## 📖 使用指南

### 1. 启动服务 (标准流程)

**第一步：启动调试浏览器**
双击运行 **`start_chrome_debug.bat`**。
- 这会打开一个独立的 Chrome 窗口。
- **首次使用请在此窗口手动登录 ChatGPT**。
- **保持此窗口开启** (可以最小化，但不能关闭)。

**第二步：启动 API 服务**
双击运行 **`run_headless.bat`**。
- 会弹出一个终端窗口显示服务启动日志。
- 当看到 `Successfully connected to Chrome!` 时，服务就绪。

### 2. 调用 API

服务默认地址: `http://localhost:8000/v1/chat/completions`

#### 示例 1: 纯文本对话 (Python)
```python
import requests

url = "http://localhost:8000/v1/chat/completions"
data = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "你好，介绍一下你自己"}]
}
response = requests.post(url, json=data)
print(response.json())
```

#### 示例 2: 图片上传与分析 (二手车案例)
要发送图片，需要构造 OpenAI 标准的**多模态消息**。
**注意**: 由于是本地服务，`image_url` 支持直接传递**本地绝对路径** (格式: `file://D:/path/to/image.png` 或直接 `D:/path/to/image.png`)。

```python
import requests
import os

images = [r"D:\photos\car1.jpg", r"D:\photos\car2.jpg"]

# 构建消息内容
content = [{"type": "text", "text": "请分析这些图片中的车辆状况"}]
for img_path in images:
    content.append({
        "type": "image_url", 
        "image_url": {"url": img_path} # 直接传本地路径
    })

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [{"role": "user", "content": content}]
}

response = requests.post("http://localhost:8000/v1/chat/completions", json=payload, timeout=120)
print(response.json())
```

### 3. 查看日志
即时对话日志会自动写入根目录下的 `chat_history.jsonl` 文件。每行是一个 JSON 对象，包含请求和响应的完整快照。

---

## ⚠️ 常见问题

- **报错 `Method Not Allowed`**: 你可能在浏览器里直接访问了 `http://localhost:8000/...`，请使用 POST 请求调用。
- **报错 `Timeout`**: 生成长文本时（如写代码），ChatGPT 响应较慢。请在客户端设置更长的超时时间 (e.g., 120s 或 240s)。
- **Cloudflare 验证**: 如果在 `start_chrome_debug.bat` 打开的窗口中看到 Cloudflare 验证，请**手动点击**过盾。服务会自动重试连接。
