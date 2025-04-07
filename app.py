from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import threading
import time
import queue
from conversation.conversation import handle_message, create_session, sessions, locks

# from conversation.generate_answer import generate_answer, check_session_timeout, sessions, locks

app = Flask(__name__, template_folder='webpage', static_folder='static')
CORS(app)  

# Session timeout (in seconds)
SESSION_TIMEOUT = 160

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_route():
    """Handle a single user question and return the model's generated response"""
    data = request.get_json()
    user_question = data.get('question')
    session_id = data.get('session_id')

    if not user_question or not session_id:
        return jsonify({'error': 'Missing question or session_id'}), 400

    # print(f"Received data: {data}")
    # print(f"User question: {user_question}, Session ID: {session_id}")

    create_session(user_question,session_id)
     
    # handle_message(user_question,session_id) 
    threading.Thread(target=handle_message, args=(user_question, session_id)).start()

    # with locks[session_id]:
    #     sessions[session_id]['last_active'] = time.time()

    #     # Wait for the model's response
    #     while sessions[session_id]['response'] is None:
    #         time.sleep(0.1)

    #     response = sessions[session_id]['response']
    #     sessions[session_id]['response'] = None

    # return jsonify({'response': response})

    # Wait for the answer to return from the queue
    session_context = sessions.get(session_id)
    response = session_context['queue'].get() 

    return jsonify({'answer': response})

@app.route('/get_answer', methods=['GET'])
def get_answer():
    """Poll for streaming responses"""
    session_id = request.args.get('session_id')
    session_context = sessions.get(session_id)

    if not session_context:
        return jsonify({'error': 'Session not found'}), 400

    # Get generated text from the queue
    try:
        generated_text = session_context['queue'].get(timeout=1)  
    except queue.Empty:
        return jsonify({'answer': None})  

    return jsonify({'answer': generated_text})


if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()  # Start the server and listen on port 5000
    app.run(host='0.0.0.0', port=5000)
