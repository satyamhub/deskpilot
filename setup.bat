@echo off
REM setup.bat - DeskPilot Setup Script for Windows
REM Run this once to set up DeskPilot

echo.
echo 🤖 DeskPilot Setup
echo ==================
echo.

REM Check Python version
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo   Python version: %python_version%

REM Check if Ollama is running
echo.
echo ✓ Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  Ollama is not running
    echo       Run in another terminal: ollama run llama3
) else (
    echo   ✅ Ollama is running on localhost:11434
)

REM Create virtual environment
echo.
echo ✓ Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   ✅ Virtual environment created
) else (
    echo   ℹ️  Virtual environment already exists
)

REM Activate virtual environment
echo.
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo ✓ Installing dependencies...
pip install -q -r requirements.txt
echo   ✅ Dependencies installed

REM Install Playwright browsers
echo.
echo ✓ Installing Playwright browsers...
python -m playwright install
echo   ✅ Playwright browsers installed

REM Verify imports
echo.
echo ✓ Verifying imports...
python -c "import playwright; import requests; print('  ✅ All imports successful')" >nul 2>&1
if errorlevel 1 (
    echo   ❌ Import error
    pause
    exit /b 1
)

echo.
echo ==================================
echo ✅ Setup complete!
echo ==================================
echo.
echo Next steps:
echo 1. Make sure Ollama is running:
echo    ^> ollama run llama3
echo.
echo 2. Activate virtual environment (if not already):
echo    ^> venv\Scripts\activate.bat
echo.
echo 3. Run DeskPilot:
echo    ^> python main.py
echo.
pause
