@echo off
echo Starting WebGPT in LOGIN MODE (Visible Browser)...
echo Please log in to ChatGPT in the opened window.
echo Once logged in, you can close this server and run 'run_headless.bat'.
echo.
python main.py --visible
pause
