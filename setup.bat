@echo off
echo Organization Management System Setup
echo =====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✓ Dependencies installed successfully!
    echo.
    echo To run the application:
    echo   python Project.py
    echo.
    echo Make sure your MySQL server is running and the database is set up.
    echo See README.md for detailed setup instructions.
) else (
    echo.
    echo ✗ Failed to install dependencies.
    echo Please check your internet connection and try again.
)

echo.
pause
