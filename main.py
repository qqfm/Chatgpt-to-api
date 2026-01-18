from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Literal
import uvicorn
import asyncio
from browser_manager import ChatGPTBrowser
import os
import argparse
import json
import datetime
from version import __version__, __release_date__

# Parse command line arguments to determine headless mode
parser = argparse.ArgumentParser()
parser.add_argument("--visible", action="store_true", help="Run browser in visible mode (headed)")
parser.add_argument("--version", action="store_true", help="Show version and exit")
# Use parse_known_args to avoid conflicts if uvicorn adds its own args later
args, _ = parser.parse_known_args()

# Show version and exit if requested
if args.version:
    print(f"WebGPT API Gateway v{__version__}")
    print(f"Release Date: {__release_date__}")
    exit(0)

def log_conversation(user_text: str, file_paths: List[str], assistant_text: str, model: str):
    """Logs the conversation to a JSONL file"""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": model,
        "request": {
            "text": user_text,
            "files": file_paths
        },
        "response": assistant_text
    }
    
    try:
        with open("chat_history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

app = FastAPI(
    title="ChatGPT-to-API",
    description="A generic OpenAI compatible API for ChatGPT Web",
    version=__version__,
)

from typing import List, Optional, Union, Any

# Global browser instance
# Default is headless unless --visible is passed
browser_manager = ChatGPTBrowser(headless=not args.visible)

class Message(BaseModel):
    role: str
    content: Union[str, List[Any]]

class ChatCompletionRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[Message]
    stream: bool = False

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str = "chatcmpl-mock"
    object: str = "chat.completion"
    created: int = 1677652288
    model: str
    choices: List[Choice]

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print(f"WebGPT API Gateway v{__version__}")
    print(f"Release: {__release_date__}")
    print("=" * 60)
    print("Starting browser...")
    await browser_manager.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("Closing browser...")
    await browser_manager.close()

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible endpoint.
    Retrieves the last user message and sends it to ChatGPT Browser.
    """
    
    # Parse the last user message to extract text and images
    last_message = next((m for m in reversed(request.messages) if m.role == "user"), None)
    
    if not last_message:
        raise HTTPException(status_code=400, detail="No user message found")

    content = last_message.content
    message_text = ""
    file_paths = []
    
    if isinstance(content, str):
        message_text = content
    elif isinstance(content, list):
        # Handle multimodal content
        for item in content:
            if item.get("type") == "text":
                message_text += item.get("text", "")
            elif item.get("type") == "image_url":
                url = item.get("image_url", {}).get("url", "")
                if url.startswith("file://"):
                    url = url[7:]
                # Basic check if file exists locally
                if os.path.exists(url):
                    file_paths.append(url)
    
    print(f"Sending to ChatGPT: {message_text[:50]}... with {len(file_paths)} files")
    
    response_text = await browser_manager.send_message(message_text, file_paths=file_paths)
    
    if response_text.startswith("Error:"):
        print(f"Backend Error: {response_text}")
        # Return a 503 Service Unavailable or 500 Internal Server Error
        # so the client knows it failed.
        raise HTTPException(status_code=503, detail=response_text)
    
    # Log the conversation
    log_conversation(message_text, file_paths, response_text, request.model)

    return ChatCompletionResponse(
        model=request.model,
        choices=[
            Choice(
                index=0,
                message=Message(role="assistant", content=response_text),
                finish_reason="stop"
            )
        ]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
