# 📱 DeskPilot Web GUI - User Guide

## 🚀 Quick Start

### 1. Install Flask

```bash
cd /home/satyaminc/Desktop/python/deskpilot
source venv/bin/activate
pip install flask
```

### 2. Start Ollama (in another terminal)

```bash
ollama run llama3
```

### 3. Launch Web GUI

```bash
# Linux/Mac:
bash run_gui.sh

# Windows:
run_gui.bat

# Or directly:
python app.py
```

### 4. Open Browser

```
http://localhost:5000
```

---

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  🤖 DeskPilot - AI Autopilot Browser Agent             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Enter command...] [Generate Plan]                    │
│                                                         │
│  ✅ Status: Ready                                      │
│                                                         │
│  📋 Generated Plan                                     │
│  ├─ Step 1: open_website - youtube.com                │
│  ├─ Step 2: wait - 2 seconds                          │
│  └─ Step 3: search - Python tutorials                 │
│                                                         │
│  [▶️ Execute] [↺ New Command]                         │
│                                                         │
│  📜 Execution History                                  │
│  ├─ "Open YouTube..." ✅ Success                       │
│  └─ "Search Google..." ❌ Failed                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 How to Use

### Step 1: Enter Command

Type a natural language command in the input field:

```
"Open YouTube and search for Python tutorials"
"Go to Google and search machine learning"
"Visit Wikipedia and find AI information"
```

### Step 2: Generate Plan

Click "Generate Plan" or press Enter.
The system will:

- Send command to Ollama LLM
- Generate JSON action plan
- Display steps for review

### Step 3: Review Plan

Look at the generated steps and verify they make sense.

### Step 4: Execute

Click "▶️ Execute" to start browser automation.
The browser will:

- Open and perform each action
- Show progress in real-time
- Complete the task

### Step 5: Check History

View all completed tasks in the execution history.

---

## 🎯 Example Workflows

### Search Workflow

```
Command: "Open Google and search Django tutorial"

Plan Generated:
1. open_website - google.com
2. search - Django tutorial

Output: Browser opens Google, searches for Django
```

### Video Search Workflow

```
Command: "Go to YouTube and find Python beginner videos"

Plan Generated:
1. open_website - youtube.com
2. wait - 2
3. search - Python beginner

Output: YouTube loads, searches for videos
```

### Multi-Step Research

```
Command: "Visit Wikipedia, search machine learning, click first result"

Plan Generated:
1. open_website - wikipedia.org
2. search - machine learning
3. click - first_result

Output: Wikipedia loads, searches, shows article
```

---

## 🎨 UI Features

### Status Indicators

- 🧠 **Planning** - Generating plan from command
- ✅ **Ready** - Plan generated, ready to execute
- ⏳ **Executing** - Running automation steps
- ✅ **Completed** - Task finished successfully
- ❌ **Error** - Something went wrong

### Action Buttons

- **Generate Plan** - Create execution plan
- **Execute** - Run the plan
- **New Command** - Reset and try another command

### Execution History

- Show all past commands
- Display success/failure status
- Timestamp and step count
- Click to see details

---

## ⚙️ Configuration

### Server Settings (app.py)

```python
app.run(
    debug=True,              # Enable debug mode
    host='0.0.0.0',         # Accept from any IP
    port=5000               # Port number
)
```

### Change Port

Edit app.py last line:

```python
app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)  # Port 8000
```

### Disable Debug Mode (Production)

```python
app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)
```

---

## 🔧 API Endpoints

The GUI uses these REST APIs:

### POST /api/plan

Generate execution plan

```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"command": "Open YouTube"}'
```

### POST /api/execute

Start executing the plan

```bash
curl -X POST http://localhost:5000/api/execute
```

### GET /api/status

Get current execution status

```bash
curl http://localhost:5000/api/status
```

### GET /api/history

Get execution history

```bash
curl http://localhost:5000/api/history
```

### POST /api/clear-history

Clear execution history

```bash
curl -X POST http://localhost:5000/api/clear-history
```

---

## 🐛 Troubleshooting

### "Connection refused"

```
❌ Ollama is not running
✅ Solution: Run 'ollama run llama3' in another terminal
```

### "Failed to generate plan"

```
❌ Ollama connection failed
✅ Solution:
   1. Make sure Ollama is running
   2. Check localhost:11434 is accessible
   3. Verify llama3 model is installed
```

### "Port 5000 already in use"

```
❌ Another app using port 5000
✅ Solutions:
   1. Kill process: lsof -ti:5000 | xargs kill -9
   2. Use different port: edit app.py, change port=5000
```

### Browser doesn't open

```
❌ Playwright issue
✅ Solutions:
   1. Reinstall: python -m playwright install
   2. Check headless=False in browser.py
   3. Some websites block automation
```

---

## 🎓 Advanced Usage

### Using Custom LLM Models

Edit brain.py:

```python
OLLAMA_API_URL = "http://localhost:11434/api/generate"
call_ollama(prompt, model="mistral")  # Change model
```

### Adding Custom Actions

Edit executor.py to add new action types:

```python
elif action == "screenshot":
    await browser_mgr.screenshot()
```

### Extending API

Add new endpoints to app.py:

```python
@app.route('/api/custom', methods=['POST'])
def custom_action():
    # Your custom logic here
    return jsonify({'result': 'success'})
```

---

## 📊 Performance Tips

1. **Keep commands simple** - Better LLM results
2. **Wait between actions** - Add "wait" steps for slow sites
3. **Close browser** - Add "close_browser" at end of plan
4. **Monitor memory** - Browser can use 300-500MB
5. **Use specific selectors** - Click actions work better with unique IDs

---

## 🔐 Security Notes

- ✅ All processing is local
- ✅ No data sent to external services
- ✅ Safe JSON parsing (no eval)
- ⚠️ Open to localhost only by default
- ⚠️ Debug mode disabled in production

### Secure Deployment

For production use:

```python
app.run(
    debug=False,
    use_reloader=False,
    host='127.0.0.1',  # Local only
    port=5000,
    ssl_context='adhoc'  # HTTPS
)
```

---

## 📞 Support

Problems? Check:

- [Instructions.md](Instructions.md) - Setup guide
- [README.md](README.md) - Project overview
- [EXAMPLES.md](EXAMPLES.md) - Example commands
- Code comments in each module

---

## 🚀 Next Steps

1. Try simple commands first
2. Check browser automation works
3. Explore execution history
4. Try complex multi-step tasks

Happy automating! 🤖✨
