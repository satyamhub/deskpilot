# DeskPilot - AI Autopilot Browser Agent

Build AI-powered browser automation with local LLM reasoning (no API keys needed).

## 🎯 Overview

DeskPilot is an AI autopilot agent that:

1. Takes natural language commands from users
2. Uses Ollama (llama3) LLM to break tasks into steps
3. Executes steps using Playwright browser automation
4. Returns structured JSON action plans (no eval)

**Example:**

- Input: "Open YouTube and search for DSA problems"
- Output: Browser opens YouTube → searches "DSA problems"

## 🏗️ Architecture

```
user input
    ↓
[planner.py] → LLM generates JSON plan
    ↓
[executor.py] → Browser automation
    ↓
task complete
```

### Modules

- **brain.py** - Ollama LLM integration (HTTP to localhost:11434)
- **planner.py** - Converts natural language to JSON action steps
- **browser.py** - Playwright wrapper (async)
- **executor.py** - Runs action steps sequentially
- **main.py** - CLI entry point and command loop

## ⚙️ Installation & Setup

### 1. Install Ollama

```bash
# Download from: https://ollama.ai
# Or use package manager:
brew install ollama        # macOS
# For Linux/Windows, visit https://ollama.ai/download
```

### 2. Start Ollama with llama3

```bash
ollama run llama3
# Ollama will download llama3 model and serve on http://localhost:11434
# Keep this terminal running
```

### 3. Clone/Setup DeskPilot

```bash
cd /path/to/deskpilot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

```bash
playwright install
```

## 🚀 Usage

### Start DeskPilot

```bash
python main.py
```

### Example Commands

```
🎯 Enter command: Open YouTube and search for DSA problems
🎯 Enter command: Go to GitHub and find Python projects
🎯 Enter command: Search for machine learning tutorials on Google
🎯 Enter command: help
🎯 Enter command: quit
```

### Workflow

1. Enter natural language command
2. DeskPilot generates a step plan using Ollama
3. Review the plan (yes/no/quit)
4. Browser automation executes each step
5. Browser opens in GUI mode so you can see actions

## 📋 Supported Actions

The planner can generate these actions:

```json
{
  "action": "open_website",
  "target": "youtube.com"
}
```

```json
{
  "action": "search",
  "query": "DSA problems"
}
```

```json
{
  "action": "click",
  "target": "CSS_SELECTOR"
}
```

```json
{
  "action": "type_text",
  "target": "CSS_SELECTOR",
  "text": "text to type"
}
```

```json
{
  "action": "wait",
  "seconds": 2
}
```

```json
{
  "action": "close_browser"
}
```

## 🔧 Configuration

### Ollama Settings (brain.py)

- **OLLAMA_API_URL**: `http://localhost:11434/api/generate`
- **Default Model**: `llama3`
- **Timeout**: 30 seconds

### Browser Settings (browser.py)

- **Headless Mode**: `False` (GUI visible)
- **Timeout**: 10 seconds for page loads
- **Wait Policy**: `networkidle` for full page load

## 📝 Project Structure

```
deskpilot/
├── main.py              # Entry point
├── brain.py             # Ollama LLM integration
├── planner.py           # Task to JSON steps
├── browser.py           # Playwright automation
├── executor.py          # Execute steps
├── requirements.txt     # Dependencies
├── Instructions.md      # This file
└── README.md           # Project overview
```

## 🐛 Troubleshooting

### "Cannot connect to Ollama"

- Make sure `ollama run llama3` is running in another terminal
- Check that Ollama is accessible at `http://localhost:11434`
- Try: `curl http://localhost:11434/api/tags`

### "Playwright not found"

- Run: `playwright install`
- Make sure chromium is download properly

### LLM returns invalid JSON

- The planner will show the raw response (first 200 chars)
- Ollama might need more context or the prompt needs adjustment
- Try simpler commands first

### Browser doesn't load page

- Some websites block Playwright automation
- Try adding wait steps to allow more time
- Check browser console for errors

## 💡 Tips & Tricks

1. **Better Results**: Be specific in commands
   - ✅ "Open YouTube and search for Python tutorials"
   - ❌ "Do something online"

2. **Complex Tasks**: Break into multiple commands
   - Instead of one huge task, run it step by step

3. **Website Blocks**: Some sites detect automation
   - Use `wait` actions to slow down
   - Try different selectors for clicking

4. **Debug Plans**: Read the JSON plan before execution
   - Make sure steps make sense
   - Edit mental note for next attempts

## 🔐 Security Notes

- **No API Keys**: Uses local Ollama, no external APIs
- **No Eval**: All JSON parsing is safe (uses json library)
- **Local Only**: All processing happens on your machine
- **No Data Sent**: Nothing leaves your computer

## 📚 Dependencies

- `playwright>=1.40.0` - Browser automation
- `requests>=2.31.0` - HTTP calls to Ollama
- `ollama` - Local LLM (installed separately)

## 🎓 Learning Resources

- [Playwright Docs](https://playwright.dev/python/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Llama 3 Model](https://ollama.ai)

## 🚧 Future Enhancements

- [ ] Support for multiple browser tabs
- [ ] Screenshot capture for validation
- [ ] OCR for visual element finding
- [ ] Action recording and playback
- [ ] Database for storing task history
- [ ] Support for other LLMs (OpenAI, Anthropic)
- [ ] Parallel action execution
- [ ] Mobile browser support

## 📄 License

See LICENSE file for details.

---

**Happy Automating! 🚀**

Questions? Issues? Code improvements? Feel free to contribute!
