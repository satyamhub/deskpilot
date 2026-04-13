"""
app.py - DeskPilot Web GUI
Flask application for web-based DeskPilot interface
"""

from flask import Flask, render_template, request, jsonify
import threading
import json
from datetime import datetime
from planner import generate_plan
from executor import execute_plan_sync

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Store execution state
execution_state = {
    'running': False,
    'current_step': 0,
    'total_steps': 0,
    'status': 'idle',
    'last_command': '',
    'last_plan': None,
    'history': [],
    'cancel_requested': False,
    'execution_thread': None
}


@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')


@app.route('/api/plan', methods=['POST'])
def create_plan():
    """Generate a plan from user command"""
    if execution_state['running']:
        return jsonify({'error': 'Already executing a task'}), 400
    
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'error': 'Command cannot be empty'}), 400
    
    execution_state['last_command'] = command
    execution_state['status'] = 'planning'
    
    # Generate plan
    plan = generate_plan(command)
    
    if plan is None:
        return jsonify({'error': 'Failed to generate plan. Make sure Ollama is running.'}), 500
    
    execution_state['last_plan'] = plan
    execution_state['status'] = 'ready'
    
    return jsonify({
        'command': command,
        'plan': plan,
        'steps': len(plan)
    })


@app.route('/api/execute', methods=['POST'])
def execute():
    """Execute the generated plan"""
    if execution_state['running']:
        return jsonify({'error': 'Already executing'}), 400
    
    if execution_state['last_plan'] is None:
        return jsonify({'error': 'No plan to execute. Generate a plan first.'}), 400
    
    execution_state['running'] = True
    execution_state['status'] = 'executing'
    execution_state['current_step'] = 0
    execution_state['total_steps'] = len(execution_state['last_plan'])
    execution_state['cancel_requested'] = False
    
    # Execute in background thread
    thread = threading.Thread(target=_execute_plan_background)
    thread.daemon = True
    thread.start()
    execution_state['execution_thread'] = thread
    
    return jsonify({'status': 'executing'})


def _execute_plan_background():
    """Execute plan in background"""
    try:
        success = execute_plan_sync(execution_state['last_plan'])
        
        # Add to history
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': execution_state['last_command'],
            'success': success,
            'steps': len(execution_state['last_plan'])
        }
        execution_state['history'].append(history_entry)
        
        if success:
            execution_state['status'] = 'completed'
        else:
            execution_state['status'] = 'completed_with_errors'
    
    except Exception as e:
        execution_state['status'] = 'error'
        print(f"ERROR: {e}")
    
    finally:
        execution_state['running'] = False


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current execution status"""
    return jsonify({
        'running': execution_state['running'],
        'status': execution_state['status'],
        'current_step': execution_state['current_step'],
        'total_steps': execution_state['total_steps'],
        'command': execution_state['last_command']
    })


@app.route('/api/cancel', methods=['POST'])
def cancel():
    """Cancel current execution"""
    if not execution_state['running']:
        return jsonify({'error': 'No task is running'}), 400
    
    execution_state['cancel_requested'] = True
    execution_state['running'] = False
    execution_state['status'] = 'cancelled'
    
    return jsonify({'status': 'cancelled', 'message': 'Task cancellation requested'})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get execution history"""
    return jsonify({'history': execution_state['history']})


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear execution history"""
    execution_state['history'] = []
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 DeskPilot Web GUI")
    print("="*60)
    print("\n🌐 Web Interface: http://localhost:5000")
    print("📝 Make sure Ollama is running: ollama run llama3\n")
    print("="*60 + "\n")
    
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
