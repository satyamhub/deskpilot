"""
brain.py - LLM reasoning module
Supports both Claude API and Ollama backends
"""

import requests
import json
from typing import Dict, Optional
import os

# Backend selection
LLM_BACKEND = os.getenv("LLM_BACKEND", "claude").lower()  # "claude" or "ollama"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
OLLAMA_API_URL = "http://localhost:11434/api/generate"


def call_claude(prompt: str) -> Optional[str]:
    """
    Call Claude API with a prompt and return the response.
    Uses environment variable CLAUDE_API_KEY for authentication.
    Falls back to demo mode if key is not available.
    
    Args:
        prompt: The prompt to send to Claude
    
    Returns:
        The response text from Claude, or None if request fails
    """
    if not CLAUDE_API_KEY:
        # Demo mode - return fast mock responses
        # Extract user command from the planning prompt
        if "User Command:" in prompt:
            user_command = prompt.split("User Command:")[-1].strip().split("\n")[0]
        else:
            user_command = prompt
        return call_claude_demo(user_command)
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
    
    except ImportError:
        print("WARNING: anthropic package not installed. Using demo mode.")
        return call_claude_demo(prompt)
    except Exception as e:
        print(f"ERROR: Claude API error: {e}")
        if "User Command:" in prompt:
            user_command = prompt.split("User Command:")[-1].strip().split("\n")[0]
        else:
            user_command = prompt
        return call_claude_demo(user_command)


def call_claude_demo(prompt: str) -> str:
    """
    Demo mode - return instant mock responses without API calls.
    Intelligently generates plans based on command keywords.
    Parses actions in order of appearance.
    """
    import re
    
    prompt_lower = prompt.lower()
    actions = []
    processed = 0
    
    # Process commands in order of appearance
    while processed < len(prompt_lower):
        remaining = prompt_lower[processed:]
        
        # Check for open/visit/go actions
        open_match = re.match(r'\s*(open|visit|go)\s+([^\s\.]+(?:\.[^\s]+)?)', remaining)
        if open_match:
            url = open_match.group(2)
            # Normalize URLs
            if url == "youtube":
                url = "youtube.com"
            elif url == "google":
                url = "google.com"
            elif url == "github":
                url = "github.com"
            actions.append({"action": "open_website", "target": url})
            processed += open_match.end()
            continue
        
        # Check for click actions
        click_match = re.match(r'\s*(?:and\s+)?click\s+(?:on\s+)?([^,\.]+?)(?=\s+(?:and\s+|type\s+)|,|$)', remaining)
        if click_match:
            element = click_match.group(1).strip()
            actions.append({"action": "click", "target": element})
            processed += click_match.end()
            continue
        
        # Check for type/enter actions: "type [text] in [field]" or "enter [text] in [field]"
        type_match = re.match(r'\s*(?:and\s+)?(?:type|enter)\s+(.+?)\s+in\s+(\w+(?:\s+\w+)*)', remaining, re.IGNORECASE)
        if type_match:
            text = type_match.group(1).strip()
            field = type_match.group(2).strip()
            actions.append({"action": "type_text", "target": field, "text": text})
            processed += type_match.end()
            continue
        
        # Default fallback if nothing matched - skip to find next action
        next_action_pos = len(remaining)
        for keyword in ["open", "click", "type", "and click", "and type"]:
            pos = remaining.find(keyword, 1)  # Skip position 0 to avoid immediate match
            if pos > 0:
                next_action_pos = min(next_action_pos, pos)
        
        if next_action_pos == len(remaining):
            break
        processed += next_action_pos
    
    # Default fallback if no actions were parsed
    if not actions:
        actions = [{"action": "open_website", "target": "google.com"}]
    
    return json.dumps(actions)


def call_ollama(prompt: str, model: str = "llama3") -> Optional[str]:
    """
    Call Ollama LLM with a prompt and return the response.
    
    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (default: llama3)
    
    Returns:
        The complete response text from Ollama, or None if request fails
    """
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "").strip()
    
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return None
    except requests.exceptions.Timeout:
        print("ERROR: Ollama request timed out")
        return None
    except Exception as e:
        print(f"ERROR: Ollama API error: {e}")
        return None


def call_llm(prompt: str) -> Optional[str]:
    """
    Call the configured LLM backend (Claude or Ollama).
    
    Args:
        prompt: The prompt to send to the LLM
    
    Returns:
        The response text from the LLM
    """
    if LLM_BACKEND == "claude":
        return call_claude(prompt)
    else:
        return call_ollama(prompt)


def extract_json_from_response(response: str) -> Optional[Dict]:
    """
    Extract JSON from LLM response text.
    Safely parse JSON without using eval().
    
    Args:
        response: The response text from Ollama
    
    Returns:
        Parsed JSON object, or None if parsing fails
    """
    try:
        # Try to find JSON in the response
        # Look for content between { } or [ ]
        start_idx = response.find('[')
        if start_idx == -1:
            start_idx = response.find('{')
        
        if start_idx == -1:
            return None
        
        # Find the closing bracket
        end_idx = response.rfind(']')
        if end_idx == -1:
            end_idx = response.rfind('}')
        
        if end_idx == -1 or end_idx <= start_idx:
            return None
        
        json_str = response[start_idx:end_idx + 1]
        parsed = json.loads(json_str)
        return parsed
    
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON from response: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error parsing response: {e}")
        return None


def reason(query: str) -> Optional[str]:
    """
    General reasoning function for any query.
    
    Args:
        query: The question or prompt
    
    Returns:
        The reasoning result from LLM
    """
    return call_llm(query)
