import threading
import queue
from conversation.agent import Agent
import time
from conversation.prompt import get_agent_prompt

# Global session data and locks (imported from agent.py)
from conversation.agent import sessions, locks

# Session timeout (in seconds)
SESSION_TIMEOUT = 60

system_prompt = get_agent_prompt()
historical_messages = []  
agent = Agent(system_prompt, historical_messages)

def check_session_timeout(session_id):
    """Check if the session has timed out and close the session"""
    while True:
        time.sleep(SESSION_TIMEOUT)
        if session_id in sessions:
            with locks[session_id]:
                if time.time() - sessions[session_id]['last_active'] > SESSION_TIMEOUT:
                    sessions[session_id]['queue'].put(None)
                    del sessions[session_id]
                    del locks[session_id]
                    break

def create_session(user_message, session_id):
    """Create a session if it doesn't exist"""
    if session_id not in sessions:
        sessions[session_id] = {
            'queue': queue.Queue(),
            'context': '',  
            'response': None,  
            'last_active': time.time() 
        }
        locks[session_id] = threading.Lock()

def handle_message(user_message, session_id):
    return agent.run_turn(user_message, session_id)
