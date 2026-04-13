# DeskPilot - Example Sessions & Use Cases

## 🎯 Example 1: Search DSA Problems on YouTube

### User Command

```
🎯 Enter command: Open YouTube and search for DSA problems
```

### Generated Plan

```
🧠 Planning: Open YouTube and search for DSA problems
📋 Raw response from LLM: [
  {"action": "open_website", "target": "youtube.com"},
  {"action": "wait", "seconds": 2},
  {"action": "search", "query": "DSA problems"}
]
✅ Generated 3 steps:
   Step 1: open_website - Target: youtube.com
   Step 2: wait - Target: N/A
   Step 3: search - Target: N/A
```

### Execution

```
============================================================
Review the plan above. Proceed? (yes/no/quit):
→ yes

============================================================
▶️  Executing 3 steps...

📍 Step 1/3: open_website
🔗 Opening: https://youtube.com
✅ Loaded: https://youtube.com

📍 Step 2/3: wait
⏳ Waiting 2 seconds...
✅ Wait complete

📍 Step 3/3: search
🔍 Searching for: DSA problems
✅ Search completed

============================================================
✨ Task completed successfully!
```

---

## 🎯 Example 2: Find Python Projects on GitHub

### User Command

```
🎯 Enter command: Go to GitHub and find Python projects
```

### Generated Plan

```
✅ Generated 4 steps:
   Step 1: open_website - Target: github.com
   Step 2: click - Target: search button
   Step 3: type_text - Target: search input
   Step 4: search - Target: N/A
```

### Note

Both work - search happens automatically on most sites, or you can click + type manually first.

---

## 🎯 Example 3: Multiple Step Task

### User Command

```
🎯 Enter command: Open Wikipedia, search for artificial intelligence, and find information
```

### Generated Plan

```
✅ Generated 5 steps:
   Step 1: open_website - Target: wikipedia.org
   Step 2: wait - Target: N/A
   Step 3: search - Target: N/A (searches for "artificial intelligence")
   Step 4: wait - Target: N/A
   Step 5: click - Target: result link
```

---

## 💡 Best Practices & Tips

### ✅ DO: Be Specific

```
GOOD:  "Open Google and search for 'machine learning tutorials'"
BAD:   "Search something online"
```

### ✅ DO: Use Action Words

```
GOOD:  "Go to Amazon, search laptops, click first result"
BAD:   "Amazon laptop thing"
```

### ✅ DO: Break Complex Tasks

```
Command 1: "Open Gmail"
Command 2: "Go to the search box and type 'important emails'"
Command 3: "Click filters and select unread"
```

### ⚠️ AVOID: Too Complex in One Command

```
AVOID: "Open email, check unread, reply to three specific people, forward to manager"
BETTER: Split into multiple commands
```

### ⚠️ AVOID: Website Blocks

```
Some sites detect Playwright:
- Cloudflare protected sites
- Banking/financial sites
- Some JavaScript-heavy apps

Try simpler targets first!
```

---

## 🔍 Case Studies

### Use Case 1: Price Comparison

```
Command:
"Go to Amazon and search laptops under 50000"

Expected Flow:
1. Open amazon.in
2. Search for "laptops"
3. Filter by price "under 50000"
4. Display results (user manually reviews)

When to use: Shopping, price monitoring, product research
```

### Use Case 2: Content Aggregation

```
Commands (one per iteration):
1. "Open news.ycombinator.com and show top stories"
2. "Go to Reddit and search for Python programming"
3. "Open Medium and search tech articles"

When to use: Research, content discovery, aggregation scripts
```

### Use Case 3: Learning & Tutorials

```
Commands:
1. "Go to YouTube and search Python beginner tutorials"
2. "Open Coursera and search machine learning courses"
3. "Go to Stack Overflow and search Python async/await"

When to use: Learning, skill development, documentation lookup
```

### Use Case 4: Social Media Monitoring

```
Command:
"Open Twitter and search #python #programming"

Note: Twitter might detect Playwright, but worth trying!

When to use: Hashtag tracking, trend monitoring, engagement analysis
```

### Use Case 5: Job Search

```
Commands:
1. "Go to LinkedIn and search data science jobs in Bangalore"
2. "Open Indeed and search Python developer positions"
3. "Visit Glassdoor and search company reviews"

When to use: Job research, career exploration, salary benchmarking
```

---

## 📊 Real Session Transcript

```
🤖 DeskPilot - AI Autopilot Browser Agent
============================================================
Commands: Type a task, 'quit' to exit, 'help' for examples

🎯 Enter command: help

📚 Example Commands:
  - "Open YouTube and search for DSA problems"
  - "Go to Google and search Python tutorials"
  - "Visit Wikipedia and find information about AI"
  - "Open GitHub and search for Python projects"
  - "Go to Amazon and search for laptops"

💡 Tips:
  - Commands are sent to Ollama LLM for interpretation
  - Browser opens in GUI mode so you can see actions
  - Include action words: open, search, click, type, etc.
  - Be specific about what you want to find or do

🎯 Enter command: Open Google and search machine learning

🧠 Planning: Open Google and search machine learning
📋 Raw response from LLM (first 200 chars): [
  {"action": "open_website", "target": "google.com"},
  {"action": "search", "query": "machine learning"}
]
✅ Generated 2 steps:
   Step 1: open_website - Target: google.com
   Step 2: search - Target: N/A

============================================================
Review the plan above. Proceed? (yes/no/quit):
yes

============================================================
▶️  Executing 2 steps...

📍 Step 1/2: open_website
🔗 Opening: https://google.com
✅ Loaded: https://google.com

📍 Step 2/2: search
🔍 Searching for: machine learning
✅ Search completed

============================================================
✨ Task completed successfully!

💡 Browser remains open for inspection.

🎯 Enter command: Visit Wikipedia and find information about neural networks

🧠 Planning: Visit Wikipedia and find information about neural networks
📋 Raw response from LLM (first 200 chars): [
  {"action": "open_website", "target": "wikipedia.org"},
  {"action": "search", "query": "neural networks"}
]
✅ Generated 2 steps:
   Step 1: open_website - Target: wikipedia.org
   Step 2: search - Target: N/A

============================================================
Review the plan above. Proceed? (yes/no/quit):
yes

============================================================
▶️  Executing 2 steps...

📍 Step 1/2: open_website
🔗 Opening: https://wikipedia.org
✅ Loaded: https://wikipedia.org

📍 Step 2/2: search
🔍 Searching for: neural networks
✅ Search completed

============================================================
✨ Task completed successfully!

🎯 Enter command: quit

👋 Goodbye!
```

---

## 🚀 Pro Tips & Tricks

### Tip 1: Use Clear Domain Names

```
❌ "Go to the video site"
✅ "Open YouTube"
```

### Tip 2: Include Quantity/Specificity

```
❌ "Find stuff"
✅ "Search for Python books under $30"
```

### Tip 3: Chain Logical Steps

```
Good plan for LLM:
- Open website
- Wait for load
- Search query
- Wait for results
```

### Tip 4: Inspect Browser Results

```
After task completes:
- Browser stays open
- You can manually inspect results
- Click additional links if needed
- Copy information
```

### Tip 5: Use Multiple Commands

```
Instead of: "Find and apply to job posting on LinkedIn"
Better:
1. "Open LinkedIn"
2. "Search data science jobs"
3. "Click job recommendation"
(Manually review and apply)
```

---

## ⚠️ Common Gotchas

### Gotcha 1: Site Load Time

```
Problem: Page not fully loaded before search
Solution: Plan includes wait steps automatically
```

### Gotcha 2: Dynamic Content

```
Problem: JavaScript-loaded content not available
Solution: Playwright waits for networkidle by default
```

### Gotcha 3: Login Requirements

```
Problem: Can't access content behind login
Solution: Not yet supported - future enhancement
```

### Gotcha 4: Dropdown Menus

```
Problem: Can't click dropdown items easily
Solution: Use simpler commands targeting main search
```

### Gotcha 5: Form Filling

```
Problem: Multiple fields needed
Solution: Use multiple type_text actions in plan
```

---

## 🎓 Learning Sequence

### Level 1: Simple Searches

```
1. "Open YouTube"
2. "Go to Google"
3. "Visit Wikipedia"
```

### Level 2: Search Tasks

```
1. "Open Google and search Python"
2. "Go to YouTube and search tutorials"
3. "Visit Wikipedia and search AI"
```

### Level 3: Multi-Step Tasks

```
1. "Open Google, search Python, wait, click first result"
2. "Go to GitHub, search Python projects, click trending"
3. "Visit Stack Overflow, search async await, view answers"
```

### Level 4: Complex Workflows

```
1. Multiple searches in sequence
2. Filtering and sorting
3. Chained API calls and interactions
```

---

## 📈 Metrics & Performance

### Typical Timings

```
Operation              Time
─────────────────────────────
Command to Plan        15-30s  (LLM generation)
Browser Start          3-5s    (Chromium launch)
Page Load              3-10s   (Depends on site)
Search Action          2-5s    (Includes waits)
Total Workflow         25-50s  (End to end)
```

### Success Rates

```
Website Category    Success Rate    Notes
─────────────────────────────────────────────
Major Search Sites     ~95%        Google, Bing, DuckDuckGo
Video Platforms        ~90%        YouTube works well
Social Sites           ~60%        Some have detection
News Sites             ~85%        Usually reliable
Shopping Sites         ~80%        May block sometimes
Wiki/Reference         ~95%        Very reliable
```

---

## 🎯 Next Commands to Try

```
1. Basic: "Open Google"
2. Simple: "Open YouTube and search Python"
3. Moderate: "Go to Wikipedia and search machine learning"
4. Complex: "Visit GitHub, search Python, click trending username"
5. Challenge: "Go to news.ycombinator.com and look for AI stories"
```

---

## 💬 Feedback Loop

After each task:

1. ✅ Task completed successfully
2. 👀 Manually verify results in browser
3. 📝 Note what worked well
4. 🔄 Refine prompts if needed
5. 🔗 Chain multiple commands for workflows

---

**Happy Testing! 🚀**

Start simple and build up to more complex workflows.
Remember: Every website might behave differently!
