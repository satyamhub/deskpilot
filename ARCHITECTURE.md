# DeskPilot - Architecture & Flow Diagrams

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Main.py (CLI)                        │
│           User Input Loop & Command Orchestration           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │      Planner.py                │
        │  Convert natural language      │
        │  to action plan (JSON)         │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │      Brain.py                  │
        │  HTTP to Ollama                │
        │  (localhost:11434)             │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │    Ollama LLM (llama3)         │
        │  External Process              │
        │  (Must be running)             │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │      Executor.py               │
        │  Execute action steps          │
        │  sequentially                  │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │      Browser.py                │
        │  Playwright automation         │
        │  (Async operations)            │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   Chromium Browser             │
        │   (Headless = False)           │
        │   Opens in GUI                 │
        └────────────────────────────────┘
```

## 2. Data Flow Diagram

```
                    ┌─────────────────────────┐
                    │   User Command (Text)   │
                    │  "Open YouTube and      │
                    │   search DSA problems"  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Planner Prompt       │
                    │  "Convert to JSON steps"│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   HTTP POST Request     │
                    │ localhost:11434/generate│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Ollama Processing     │
                    │   (10-30 seconds)       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   LLM Response (JSON)   │
                    │  [                      │
                    │    {...action...},      │
                    │    {...action...}       │
                    │  ]                      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   JSON Parsing          │
                    │   (Safe - no eval)      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Show Plan to User     │
                    │   "Proceed? yes/no"     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴─────────────────┐
                    │ (Yes)                        │ (No)
                    ▼                              ▼
        ┌──────────────────────┐        ┌────────────────────┐
        │ Execute Each Step:   │        │ Cancel & Retry     │
        │ • open_website       │        │ or try new command │
        │ • search             │        └────────────────────┘
        │ • click              │
        │ • type_text          │
        │ • wait               │
        │ • close_browser      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Browser Actions     │
        │  (Async)             │
        │  • Navigate pages    │
        │  • Interact with DOM │
        │  • Wait for load     │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  ✅ Task Complete    │
        │  Ready for next cmd  │
        └──────────────────────┘
```

## 3. Module Dependency Graph

```
main.py
  ├── imports: planner
  │      └── imports: brain
  │             └── imports: requests, json
  │      └── imports: executor
  │             ├── imports: asyncio
  │             └── imports: browser
  │                    └── imports: playwright.async_api

Requirements:
  ├── playwright>=1.40.0 ────────► browser.py
  └── requests>=2.31.0 ──────────► brain.py
```

## 4. Execution Flow (Step by Step)

```
START
  │
  ├─ main.py starts
  │    └─ prints header & prompts for input
  │
  ├─ User enters: "Open YouTube and search DSA"
  │
  ├─ generate_plan() called
  │    ├─ create_planning_prompt() builds prompt
  │    ├─ call_ollama() sends HTTP request
  │    │    └─ waits for LLM response (10-30s)
  │    └─ extract_json_from_response() parses JSON
  │         └─ returns plan list
  │
  ├─ Display plan to user
  │    ├─ Step 1: open_website - youtube.com
  │    └─ Step 2: search - DSA problems
  │
  ├─ User confirms: "yes"
  │
  ├─ execute_plan_sync() called
  │    ├─ get_browser_manager() starts browser
  │    │    └─ launches Chromium (non-headless)
  │    │
  │    ├─ For each step:
  │    │    ├─ Step 1: open_website()
  │    │    │    ├─ format URL
  │    │    │    ├─ call page.goto()
  │    │    │    └─ wait for networkidle
  │    │    │
  │    │    └─ Step 2: search()
  │    │         ├─ find search input
  │    │         ├─ fill query text
  │    │         ├─ press Enter
  │    │         └─ wait for results
  │    │
  │    └─ completion message
  │
  ├─ Browser remains open (for inspection)
  │
  ├─ Ready for next command
  │
  └─ Loop until user quits (or exception)

END
```

## 5. Class Diagram - BrowserManager

```
┌──────────────────────────────────────────┐
│         BrowserManager (Class)           │
├──────────────────────────────────────────┤
│ Properties:                              │
│ • browser: Browser                       │
│ • page: Page                             │
│ • playwright: Playwright                 │
├──────────────────────────────────────────┤
│ Methods:                                 │
│ • start()           → initialize browser │
│ • stop()            → close browser      │
│ • open_website(url) → navigate           │
│ • search(query)     → find & use search  │
│ • click_element()   → click selector     │
│ • type_text()       → fill text input    │
│ • wait(seconds)     → time delay         │
│ • get_page_content() → get HTML          │
└──────────────────────────────────────────┘
```

## 6. Action Types Flow

```
Execute Step
    │
    ├─ action == "open_website"
    │    └─► browser_mgr.open_website(url)
    │         └─ page.goto() + wait
    │
    ├─ action == "search"
    │    └─► browser_mgr.search(query)
    │         ├─ find search input
    │         └─ fill + enter
    │
    ├─ action == "click"
    │    └─► browser_mgr.click_element(selector)
    │         └─ locator.click()
    │
    ├─ action == "type_text"
    │    └─► browser_mgr.type_text(selector, text)
    │         ├─ click element
    │         └─ fill text
    │
    ├─ action == "wait"
    │    └─► browser_mgr.wait(seconds)
    │         └─ asyncio.sleep()
    │
    └─ action == "close_browser"
         └─► browser_mgr.stop()
              └─ close all resources
```

## 7. Error Handling Flow

```
Try Operation
    │
    ├─ ✅ Success
    │    └─ Continue to next step
    │
    └─ ❌ Exception
         ├─ Try-Catch Block
         │    └─ Print error message
         │
         ├─ Step Execution
         │    ├─ Log error
         │    └─ Continue with next step (resilient)
         │
         ├─ Plan Execution
         │    ├─ Log error
         │    └─ Continue with remaining steps
         │
         └─ Main Loop
              ├─ Catch KeyboardInterrupt
              ├─ Catch other exceptions
              └─ Prompt for retry or new command
```

## 8. State Diagram

```
          ┌──────────────────┐
          │    START         │
          └────────┬─────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Idle (Waiting for   │
        │  user command)       │
        └────────┬─────────────┘
                 │
          ┌──────┴──────────┬──────────────┐
          │                 │              │
          ▼                 ▼              ▼
    ✓ Command        × Empty/Help    × Quit
    │                │               │
    │                └─────────┬─────┘
    │                          │
    ▼                          │
┌─────────────────┐            │
│ Planning        │            │
├─────────────────┤            │
│ Call Ollama     │            │
│ Parse JSON      │            │
│ Show Plan       │            │
└────────┬────────┘            │
         │                     │
         ├─ No ──┐            │
         │       ▼            │
         │   (Back to waiting)│
         │       ◄────────────┘
         │
         ├─ Yes
         │  │
         ▼  ▼
    ┌──────────────────┐
    │ Execution        │
    ├──────────────────┤
    │ Start Browser    │
    │ Run Each Step    │
    │ Handle Errors    │
    │ Keep Browser Open│
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Complete         │
    ├──────────────────┤
    │ Show Results     │
    │ Ready for next   │
    └────────────┬─────┘
                 │
                 └─ Loop back to Idle
```

## 9. Performance Profile

```
Operation                  Time (avg)    Notes
─────────────────────────────────────────────────
Browser startup            3-5s          Chromium launch
Page load                  3-10s         networkidle wait
LLM generation             10-30s        Depends on model
Search action              2-5s          Include wait time
Click action               1-2s          Include wait time
Type action                1s            Quick operation
Wait action                variable      As specified
Total task                 20-60s        Typical workflow
```

## 10. Resource Usage

```
Memory:
├─ Base Python process:     ~50MB
├─ Playwright running:      ~100MB
├─ Browser (Chromium):      ~300-500MB
└─ Total:                   ~450-650MB

Disk:
├─ DeskPilot code:          ~100KB (all Python files)
├─ Playwright browsers:     ~300-400MB (one-time install)
├─ Ollama model (llama3):   ~4.7GB (one-time download)
└─ Total:                   ~5GB+

Network:
├─ Ollama calls:            ~1-10KB per request
├─ Website data:            Variable (pages, images)
└─ Note:                    Heavy user's internet usage
```

---

**This completes the architecture documentation. All diagrams show how DeskPilot orchestrates different components to automate browser tasks!**
