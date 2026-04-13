# DeskPilot 🤖

**AI Autopilot Browser Agent with Local LLM (No API Keys)**

DeskPilot converts natural language commands into browser automation actions. Uses Ollama (llama3) for reasoning and Playwright for browser automation—everything runs locally on your machine.

## ✨ Key Features

- 🧠 **Local LLM**: Uses Ollama + llama3 (no API keys, no internet required)
- 🔄 **Smart Planning**: Converts natural language to step-by-step actions
- 🌐 **Browser Automation**: Playwright for reliable cross-browser support
- 🛡️ **Safe JSON**: Structured action plans (no eval, no code injection)
- ⚡ **Minimal Dependencies**: Just Playwright + Requests
- 📝 **Fully Commented**: Clean, readable, production-ready code

## 🎯 Quick Start

```bash
# Install Ollama first: https://ollama.ai
ollama run llama3

# In another terminal:
pip install -r requirements.txt
playwright install
python main.py
```

Then enter commands like:

- "Open YouTube and search for DSA problems"
- "Go to GitHub and find Python projects"
- "Search for machine learning tutorials on Google"

## 📁 Architecture

```
main.py → planner.py (LLM) → executor.py → browser.py (Playwright)
```

| Module          | Purpose                                   |
| --------------- | ----------------------------------------- |
| **brain.py**    | Ollama HTTP integration (localhost:11434) |
| **planner.py**  | Natural language → JSON action plan       |
| **browser.py**  | Playwright wrapper (async operations)     |
| **executor.py** | Sequential step execution                 |
| **main.py**     | CLI loop & orchestration                  |

## 📋 Supported Actions

- `open_website` - Open a URL
- `search` - Search on current page
- `click` - Click elements by selector
- `type_text` - Type into fields
- `wait` - Wait seconds
- `close_browser` - Close browser

## 🔧 Configuration

All defaults work out of the box:

- Ollama URL: `http://localhost:11434`
- Model: `llama3`
- Browser: Chromium (headless: false)

See **Instructions.md** for detailed setup and troubleshooting.

## 📦 Dependencies

```
playwright>=1.40.0    # Browser automation
requests>=2.31.0      # HTTP to Ollama
```

Plus: Python 3.8+, Ollama with llama3

## 🏁 Why DeskPilot?

- ✅ No API costs
- ✅ Complete privacy (local processing)
- ✅ Easy to understand code
- ✅ Extensible architecture
- ✅ Works offline

Perfect for automation, learning, and building autonomous agents!

**Full documentation**: See [Instructions.md](Instructions.md)
