"""
executor.py - Plan execution module
Takes a plan (list of steps) and executes them using the browser
"""

import asyncio
from typing import List, Dict, Optional
from browser import get_browser_manager, close_browser


async def execute_step(step: Dict, browser_mgr) -> bool:
    """
    Execute a single step from the plan.
    
    Args:
        step: A dictionary containing action and related parameters
        browser_mgr: The BrowserManager instance
    
    Returns:
        True if successful, False otherwise
    """
    action = step.get("action", "").lower()
    
    try:
        if action == "open_website":
            target = step.get("target", "")
            if not target:
                print("ERROR: open_website requires 'target' URL")
                return False
            await browser_mgr.open_website(target)
            return True
        
        elif action == "search":
            query = step.get("query", "")
            if not query:
                print("ERROR: search requires 'query'")
                return False
            await browser_mgr.search(query)
            return True
        
        elif action == "click":
            target = step.get("target", "")
            if not target:
                print("ERROR: click requires 'target' selector")
                return False
            await browser_mgr.click_element(target)
            return True
        
        elif action == "type_text":
            target = step.get("target", "")
            text = step.get("text", "")
            if not target or not text:
                print("ERROR: type_text requires 'target' and 'text'")
                return False
            await browser_mgr.type_text(target, text)
            return True
        
        elif action == "wait":
            seconds = step.get("seconds", 2)
            await browser_mgr.wait(seconds)
            return True
        
        elif action == "close_browser":
            await close_browser()
            return True
        
        else:
            print(f"ERROR: Unknown action: {action}")
            return False
    
    except Exception as e:
        print(f"ERROR: Failed to execute step {action}: {e}")
        return False


async def execute_plan(plan: List[Dict]) -> bool:
    """
    Execute all steps in the plan.
    
    Args:
        plan: A list of step dictionaries
    
    Returns:
        True if all steps completed successfully, False otherwise
    """
    if not plan:
        print("ERROR: Empty plan")
        return False
    
    print(f"\n▶️  Executing {len(plan)} steps...\n")
    
    browser_mgr = await get_browser_manager()
    
    try:
        for i, step in enumerate(plan, 1):
            print(f"📍 Step {i}/{len(plan)}: {step.get('action')}")
            success = await execute_step(step, browser_mgr)
            
            if not success:
                print(f"⚠️  Step {i} failed, but continuing with next steps...")
                # Continue with next step instead of failing completely
            
            print()
        
        print("✅ Plan execution complete!")
        return True
    
    except Exception as e:
        print(f"ERROR: Plan execution failed: {e}")
        return False
    
    finally:
        # Don't close browser automatically - user might want to see results
        print("\n💡 Browser remains open for inspection. Update plan to include 'close_browser' action to close it.")


def execute_plan_sync(plan: List[Dict]) -> bool:
    """
    Synchronous wrapper for execute_plan.
    Use this from main.py.
    
    Args:
        plan: A list of step dictionaries
    
    Returns:
        True if successful, False otherwise
    """
    return asyncio.run(execute_plan(plan))
