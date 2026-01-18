@echo off
echo Fixing Playwright installation...
pip install playwright
python -m playwright install chromium
echo.
echo Fix complete. You can now run setup_login.bat or run_headless.bat
pause
