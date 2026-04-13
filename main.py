"""
main.py - DeskPilot Entry Point
Main loop that accepts user commands and orchestrates the planning and execution
"""

from planner import generate_plan
from executor import execute_plan_sync


def print_header():
    """Print the DeskPilot header"""
    print("\n" + "=" * 60)
    print("🤖 DeskPilot - AI Autopilot Browser Agent")
    print("=" * 60)
    print("Commands: Type a task, 'quit' to exit, 'help' for examples\n")


def print_help():
    """Print example commands"""
    print("""
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
""")


def main():
    """Main loop for DeskPilot"""
    print_header()
    
    while True:
        try:
            # Get user input
            user_input = input("\n🎯 Enter command (or 'quit'/'help'): ").strip()
            
            if not user_input:
                print("⚠️  Please enter a command")
                continue
            
            if user_input.lower() == "quit":
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            # Generate plan from user command
            plan = generate_plan(user_input)
            
            if plan is None:
                print("❌ Failed to generate plan. Try again with a clearer command.")
                continue
            
            # Ask user to confirm
            print("\n" + "=" * 60)
            print("Review the plan above. Proceed? (yes/no/quit):")
            confirm = input("> ").strip().lower()
            
            if confirm in ["no", "n"]:
                print("❌ Plan cancelled")
                continue
            
            if confirm in ["quit", "q"]:
                print("👋 Goodbye!")
                break
            
            if confirm not in ["yes", "y"]:
                print("⚠️  Invalid response, assuming 'yes'")
            
            # Execute the plan
            print("\n" + "=" * 60)
            success = execute_plan_sync(plan)
            print("=" * 60)
            
            if success:
                print("\n✨ Task completed successfully!")
            else:
                print("\n⚠️  Task execution had issues")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            continue


if __name__ == "__main__":
    main()
