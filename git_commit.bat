@echo off
REM ===================================================================
REM Git Quick Commit Script for WebGPT v1.1.0
REM ===================================================================

echo.
echo ============================================================
echo   WebGPT v1.1.0 - Git Commit Script
echo ============================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo.
    echo Please install Git first:
    echo   1. winget install --id Git.Git -e --source winget
    echo   2. Or download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/6] Checking Git status...
git status

echo.
echo [2/6] Git repository information:
if exist .git (
    echo   Status: Initialized
    git log --oneline -5 2>nul || echo   Status: No commits yet
) else (
    echo   Status: Not initialized
    echo.
    echo   Do you want to initialize Git repository? (Y/N)
    set /p INIT_GIT="> "
    if /i "%INIT_GIT%"=="Y" (
        git init
        echo   Git repository initialized!
    ) else (
        echo   Skipped Git initialization
        pause
        exit /b 0
    )
)

echo.
echo [3/6] Files to be committed:
echo   - Core: main.py, browser_manager.py, version.py
echo   - Scripts: *.bat files
echo   - Tools: check_browser_status.py, find_send_button.py
echo   - Tests: test_*.py
echo   - Docs: *.md files
echo   - Config: requirements.txt, .gitignore
echo.

echo [4/6] Adding files to Git...
git add main.py
git add browser_manager.py
git add version.py
git add requirements.txt
git add .gitignore
git add *.bat
git add test_*.py
git add check_browser_status.py
git add find_send_button.py
git add verify_service.py
git add complex_test.py
git add *.md

echo   Done!

echo.
echo [5/6] Creating commit...
git commit -m "v1.1.0: Major improvements and bug fixes" -m "" -m "Features:" -m "- Add enhanced logging system with [DEBUG], [INFO], [WARNING], [ERROR]" -m "- Add browser diagnostic tool (check_browser_status.py)" -m "- Add selector finder tool (find_send_button.py)" -m "- Add automatic screenshot on errors" -m "- Add version information system" -m "" -m "Improvements:" -m "- Update send button selectors for new ChatGPT interface" -m "- Support multiple fallback selectors for robustness" -m "- Improve timeout handling (60s -> 90s)" -m "- Add page state verification before operations" -m "- Optimize response waiting logic" -m "" -m "Bug Fixes:" -m "- Fix hardcoded paths in start_chrome_debug.bat" -m "- Fix Python environment path in run_headless.bat" -m "- Fix service auto-shutdown issue" -m "- Add missing 'requests' dependency" -m "" -m "Performance:" -m "- Response time improved by 86%% (60s+ -> 8.35s)" -m "- 100%% success rate in remote LAN testing" -m "" -m "Documentation:" -m "- Add SETUP_GUIDE_CN.md" -m "- Add TROUBLESHOOTING.md" -m "- Add PROJECT_SUMMARY.md" -m "- Add CHANGELOG.md" -m "- Add GIT_COMMIT_GUIDE.md"

if %ERRORLEVEL% EQU 0 (
    echo   ✅ Commit created successfully!
) else (
    echo   ❌ Commit failed!
    pause
    exit /b 1
)

echo.
echo [6/6] Creating version tag...
git tag -a v1.1.0 -m "Version 1.1.0 - ChatGPT Interface Update Fix"

if %ERRORLEVEL% EQU 0 (
    echo   ✅ Tag v1.1.0 created!
) else (
    echo   ⚠️  Tag might already exist or creation failed
)

echo.
echo ============================================================
echo   ✅ Git Commit Complete!
echo ============================================================
echo.
echo Commit Summary:
git log -1 --oneline

echo.
echo All Tags:
git tag -l

echo.
echo Next Steps:
echo   1. Review commit: git show HEAD
echo   2. Add remote (if needed): git remote add origin [URL]
echo   3. Push code: git push -u origin main
echo   4. Push tags: git push origin v1.1.0
echo.

pause
