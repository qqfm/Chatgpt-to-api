@echo off
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_PATH%" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

if not exist "%CHROME_PATH%" (
    echo Error: Chrome not found in standard locations.
    echo Please edit this file and set CHROME_PATH to your chrome.exe
    pause
    exit /b
)

echo Starting Chrome in Remote Debugging Mode...
echo Port: 9222
echo User Data: %~dp0chrome_profile
echo.
"%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%~dp0chrome_profile"
pause
