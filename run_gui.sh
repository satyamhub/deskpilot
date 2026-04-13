#!/bin/bash
# run_gui.sh - Launch DeskPilot Web GUI
# Usage: bash run_gui.sh

echo "🤖 DeskPilot Web GUI Launcher"
echo "============================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Flask is installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Flask..."
    pip install flask -q
fi

echo "✅ Environment ready"
echo ""
echo "🌐 Starting web server..."
echo "📍 Open browser: http://localhost:5000"
echo ""
echo "⚠️  IMPORTANT: Make sure Ollama is running in another terminal!"
echo "   Run: ollama run llama3"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
