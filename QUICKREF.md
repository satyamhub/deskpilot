"""
DeskPilot - Quick Reference Guide
==================================

# PROJECT STRUCTURE

deskpilot/
├── brain.py (150 lines) - LLM integration via Ollama HTTP
├── planner.py (90 lines) - Natural language → JSON action plan
├── browser.py (200 lines) - Playwright browser automation
├── executor.py (130 lines) - Execute action steps sequentially
├── main.py (100 lines) - CLI entry point & command loop
├── requirements.txt - Dependencies (minimal: playwright, requests)
├── Instructions.md - Detailed setup & troubleshooting guide
├── README.md - Project overview & quick start
└── LICENSE - Project license

# STARTUP CHECKLIST

1. Install Ollama:
   - Visit: https://ollama.ai
   - Download for your OS (Mac/Linux/Windows)

2. Start Ollama with llama3:
   $ ollama run llama3
   (Keep this terminal running - serves on localhost:11434)

3. In new terminal, setup DeskPilot:
   $ cd deskpilot
   $ python -m venv venv
   $ source venv/bin/activate # Windows: venv\Scripts\activate
   $ pip install -r requirements.txt
   $ playwright install

4. Run DeskPilot:
   $ python main.py

5. Try a command:
   🎯 Enter command: Open YouTube and search for Python tutorials

# WORKFLOW DIAGRAM

User Input (natural language)
↓
[planner.py]
├─ Create planning prompt
├─ Call Ollama (HTTP POST localhost:11434)
├─ Extract JSON from response
└─ Validate action plan
↓
[Display 5-step plan to user]
↓
[User confirms: yes/no]
↓
[executor.py]
├─ Start browser via Playwright
├─ For each step:
│ └─ Execute action (open, search, click, type, wait)
├─ Handle timeout/errors gracefully
└─ Keep browser open for inspection
↓
[Task Complete]

# CORE FUNCTIONS

brain.py:
• call_ollama(prompt, model="llama3") → response text
• extract_json_from_response(text) → dict/list
• reason(query) → LLM response

planner.py:
• create_planning_prompt(user_command) → prompt string
• generate_plan(user_command) → list of action dicts

browser.py:
• BrowserManager class: - start() - stop() - open_website(url) - search(query) - click_element(selector) - type_text(selector, text) - wait(seconds) - get_page_content() → HTML

executor.py:
• execute_step(step, browser_mgr) → bool
• execute_plan(plan: list) → bool (async)
• execute_plan_sync(plan: list) → bool (wrapper)

main.py:
• print_header()
• print_help()
• main() → CLI loop

# ACTION TYPES (SUPPORTED BY PLANNER)

1. open_website
   {
   "action": "open_website",
   "target": "youtube.com"
   }

2. search
   {
   "action": "search",
   "query": "DSA problems"
   }

3. click
   {
   "action": "click",
   "target": ".button-class" // CSS selector
   }

4. type_text
   {
   "action": "type_text",
   "target": "input[type='search']",
   "text": "search query"
   }

5. wait
   {
   "action": "wait",
   "seconds": 2
   }

6. close_browser
   {
   "action": "close_browser"
   }

# KEY DESIGN DECISIONS

✓ Async/Await: Browser operations are async (non-blocking)
✓ Safe JSON: Uses json.loads(), no eval()
✓ Error Handling: Try-catch on each step, doesn't stop for single failures
✓ Timeouts: 10s for page loads, 30s for LLM
✓ Headless: False - users can see browser actions
✓ Modular Design: Each file has single responsibility
✓ Minimal Deps: Only playwright + requests + json (stdlib)
✓ Local Only: No API keys, no cloud services

# TROUBLESHOOTING

❌ "Cannot connect to Ollama"
→ Make sure: ollama run llama3 is running
→ Check: curl http://localhost:11434/api/tags

❌ "Playwright not found"
→ Run: playwright install
→ Check: ~/.cache/ms-playwright/ has chromium

❌ "Invalid JSON from LLM"
→ LLM might be confused
→ Try simpler commands: "Open Google"
→ Check brain.py prints first 200 chars of response

❌ "Browser doesn't load website"
→ Website might block Playwright
→ Add wait steps to slow down
→ Try simpler websites first (Google, Wikipedia)

❌ "ModuleNotFoundError"
→ Forgot to activate venv
→ Source: venv/bin/activate
→ Run: pip install -r requirements.txt

# PERFORMANCE TIPS

1. LLM generations take 10-30 seconds (depends on model)
2. Website loading depends on internet speed
3. Search queries wait for "networkidle" state
4. Complex selectors might timeout (10s limit)
5. Parallel tab support coming in v2

# SECURITY & PRIVACY

✓ No external API calls (only localhost Ollama)
✓ No data sent to cloud
✓ No telemetry or logging
✓ JSON parsing is safe (uses standard lib)
✓ Everything runs on your machine
✓ No credentials stored
✓ Open source - audit the code

# EXTENSION IDEAS

• Add OCR for screen understanding (pytesseract)
• Add mouse/keyboard automation (pyautogui)
• Add memory for learning from past tasks
• Add screenshot capture for validation
• Add multi-tab support
• Add mobile browser testing
• Add different LLM backends
• Add web UI dashboard
• Add task recording/playback
• Add database for task history

# EXAMPLE SESSION

$ python main.py

============================================================
🤖 DeskPilot - AI Autopilot Browser Agent
============================================================
Commands: Type a task, 'quit' to exit, 'help' for examples

🎯 Enter command: Open YouTube and search for cat videos
🧠 Planning: Open YouTube and search for cat videos
📋 Raw response from LLM (first 200 chars): [
{"action": "open_website", "target": "youtube.com"},
{"action": "wait", "seconds": 2},
{"action": "search", "query": "cat videos"}
]
✅ Generated 3 steps:
Step 1: open_website - Target: youtube.com
Step 2: wait - Target: N/A
Step 3: search - Target: N/A

============================================================
Review the plan above. Proceed? (yes/no/quit):
yes

============================================================
▶️ Executing 3 steps...

📍 Step 1/3: open_website
🔗 Opening: https://youtube.com
✅ Loaded: https://youtube.com

📍 Step 2/3: wait
⏳ Waiting 2 seconds...
✅ Wait complete

📍 Step 3/3: search
🔍 Searching for: cat videos
✅ Search completed

============================================================
✨ Task completed successfully!

💡 Browser remains open for inspection.

🎯 Enter command: quit
👋 Goodbye!

# NEXT STEPS

1. Install and run Ollama first
2. Set up Python virtual environment
3. Install dependencies: pip install -r requirements.txt
4. Install Playwright: playwright install
5. Run: python main.py
6. Try example commands
7. Modify prompts in planner.py for better results
8. Add more actions to executor.py
9. Integrate with your own projects
10. Contribute improvements!

# VERSION INFO

DeskPilot v1.0

- Python 3.8+
- Playwright 1.40+
- Requests 2.31+
- Ollama (any version with llama3)
- Requires: 2GB+ RAM, 5GB+ disk (for Ollama model)

# QUESTIONS?

Refer to:

- Instructions.md - Full setup guide
- Code comments - Every function documented
- README.md - Project overview

Happy Automating! 🚀
"""
