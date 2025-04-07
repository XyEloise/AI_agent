from ollama import chat
import time
from conversation.ongoingMessageManager import OngoingMessageManager

# Global session data and locks
sessions = {}
locks = {}

class Agent:
    def __init__(self, system_prompt, historical_messages):
        self.ongoing_message_manager = OngoingMessageManager(system_prompt, historical_messages)
        self.sessions = sessions  
        self.locks = locks  

    def generate_answer(self, session_id):
        """Generate a streamed answer and update the session context"""
        session_context = self.sessions.get(session_id)

        if not session_context:
            return "Session not found, cannot generate an answer"

        # Set up the streaming response
        stream = chat(
            model="llama3.2:1b",  
            messages=self.ongoing_message_manager.get_messages(),
            stream=True,
            options= {             
                "temperature": 0.7,
                "max_tokens": 100
            }
        )
        
        for chunk in stream:
            generated_text = chunk["message"]["content"]
            # print(generated_text, end="", flush=True)

            # Update the session context
            session_context['context'] += generated_text
            session_context['queue'].put(generated_text)

        self.ongoing_message_manager.add_assistant_message(session_context['context'])

        # Signal the completion
        session_context['queue'].put("END")
        

    def run_turn(self, user_query, session_id):
        """Run a turn of conversation"""
        self.ongoing_message_manager.add_user_message(user_query)
        print(self.ongoing_message_manager.get_messages())
        
        self.generate_answer(session_id)
