"""
planner.py - Task planning module
Converts natural language commands into step-by-step actions (JSON format)
"""

import json
from typing import List, Dict, Optional
from brain import call_llm, extract_json_from_response


def create_planning_prompt(user_command: str) -> str:
    """
    Create a structured prompt for the LLM to generate an action plan.
    
    Args:
        user_command: The natural language command from the user
    
    Returns:
        A formatted prompt string
    """
    prompt = f"""You are a web automation planner. Convert the following user command into a JSON list of browser automation steps.

User Command: {user_command}

Generate a JSON array where each step has:
- "action": one of ["open_website", "search", "click", "type_text", "wait", "close_browser"]
- "target": the URL, element selector, or other target (optional for some actions)
- "query" or "text": the search query or text to type (if applicable)

Example format:
[
  {{"action": "open_website", "target": "youtube.com"}},
  {{"action": "search", "query": "DSA problems"}},
  {{"action": "wait"}},
  {{"action": "click", "target": "first_result"}}
]

IMPORTANT: Return ONLY valid JSON, no additional text. Start with [ and end with ].
"""
    return prompt


def generate_plan(user_command: str) -> Optional[List[Dict]]:
    """
    Convert a user command into an action plan.
    
    Args:
        user_command: The natural language command
    
    Returns:
        A list of action dictionaries, or None if planning fails
    """
    print(f"🧠 Planning: {user_command}")
    
    prompt = create_planning_prompt(user_command)
    response = call_llm(prompt)
    
    if response is None:
        print("ERROR: Failed to get response from LLM")
        return None
    
    print(f"📋 Raw response from LLM (first 200 chars): {response[:200]}...")
    
    # Extract and validate JSON
    plan = extract_json_from_response(response)
    
    if plan is None:
        print("ERROR: Failed to extract valid JSON from LLM response")
        return None
    
    # Validate plan structure
    if not isinstance(plan, list):
        print("ERROR: Plan should be a list of steps")
        return None
    
    print(f"✅ Generated {len(plan)} steps:")
    for i, step in enumerate(plan, 1):
        print(f"   Step {i}: {step.get('action', 'unknown')} - Target: {step.get('target', 'N/A')}")
    
    return plan
