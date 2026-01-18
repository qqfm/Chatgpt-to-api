# WebGPT - ChatGPT to OpenAI API Wrapper

This project creates a local server that wraps the ChatGPT web interface into an OpenAI-compatible API (similar to `llama-server`).

## Prerequisites

- Python 3.8+
- Google Chrome or Chromium (installed automatically by Playwright)

## Installation

1.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Install Playwright browsers:
    ```bash
    playwright install chromium
    ```

## Usage

1.  Run the server:
    ```bash
    python main.py
    ```
    Or simply double-click `start_server.bat`.

2.  **Important**: A browser window will open.
    - **Log in** to your ChatGPT account in this window.
    - Keep this window open (you can minimize it, but do not close it).

3.  The API is now available at `http://localhost:8000/v1/chat/completions`.

## API Example

You can use `curl` or any OpenAI-compatible client (like `chatbox` or `openai-python`).

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
  }'
```

## How if works

- It uses **Playwright** to control a real Chrome browser instance.
- It finds the chat input box on `chatgpt.com`, types your message, and clicks send.
- It waits for the response to finish generating and returns the text.
