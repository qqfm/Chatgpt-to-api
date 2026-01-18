@echo off
echo Starting WebGPT Server (CDP Mode)...
echo Connecting to open Chrome on port 9222...
echo.
echo Starting API server in a new window...
start "WebGPT API Server" cmd /k "C:\GPTAPI\.venv\Scripts\python.exe main.py"
echo.
echo API server is starting in a separate window.
echo Once you see "Uvicorn running on http://0.0.0.0:8000", the service is ready.
echo.
pause
