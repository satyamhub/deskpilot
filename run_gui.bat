@echo off
REM run_gui.bat - Launch DeskPilot Web GUI on Windows
REM Usage: run_gui.bat

echo.
echo 🤖 DeskPilot Web GUI Launcher
echo ============================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Installing Flask...
    pip install flask -q
)

echo ✅ Environment ready
echo.
echo 🌐 Starting web server...
echo 📍 Open browser: http://localhost:5000
echo.
echo ⚠️  IMPORTANT: Make sure Ollama is running in another terminal!
echo    Run: ollama run llama3
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
