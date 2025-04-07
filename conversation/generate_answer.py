from ollama import chat
import time

sessions = {}
locks = {}

# Session timeout (in seconds)
SESSION_TIMEOUT = 60

def check_session_timeout(session_id):
    """Check if the session has timed out and close the session"""
    while True:
        time.sleep(SESSION_TIMEOUT)
        with locks[session_id]:
            if time.time() - sessions[session_id]['last_active'] > SESSION_TIMEOUT:
                sessions[session_id]['queue'].put(None)
                del sessions[session_id]
                del locks[session_id]
                break

def generate_answer(user_question, session_id):
    """Generate a streamed answer and update the session context"""
    # Get the session state
    session_context = sessions[session_id]

    if not session_context:
        return "Session not found, cannot generate an answer"
    
    # Set up the streaming response
    stream = chat(
        model="llama3.2:1b",  
        messages=[{"role": "user", "content": user_question}],
        stream=True  # Enable streaming response
    )
    
    for chunk in stream:
        generated_text = chunk["message"]["content"]
        print(generated_text, end="", flush=True)
            
        # Update the session context
        session_context['context'] += generated_text
        session_context['queue'].put(generated_text)

    # completion signal 
    session_context['queue'].put("END")  