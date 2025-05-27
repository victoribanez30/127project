@echo off
echo Starting Organization Management System...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

python Project.py
pause
