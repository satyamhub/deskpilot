#!/bin/bash
# setup.sh - DeskPilot Setup Script
# Run this once to set up DeskPilot

echo "🤖 DeskPilot Setup"
echo "=================="
echo ""

# Check Python version
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

python_version=$(python3 --version | awk '{print $2}')
echo "  Python version: $python_version"

# Check if Ollama is running
echo ""
echo "✓ Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "  ✅ Ollama is running on localhost:11434"
else
    echo "  ⚠️  Ollama is not running"
    echo "      Run in another terminal: ollama run llama3"
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✅ Virtual environment created"
else
    echo "  ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  ✅ Dependencies installed"

# Install Playwright browsers
echo ""
echo "✓ Installing Playwright browsers..."
python -m playwright install -q
echo "  ✅ Playwright browsers installed"

# Verify imports
echo ""
echo "✓ Verifying imports..."
python3 -c "import playwright; import requests; print('  ✅ All imports successful')" 2>/dev/null || {
    echo "  ❌ Import error"
    exit 1
}

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running:"
echo "   % ollama run llama3"
echo ""
echo "2. Activate virtual environment (if not already):"
echo "   % source venv/bin/activate"
echo ""
echo "3. Run DeskPilot:"
echo "   % python main.py"
echo ""
