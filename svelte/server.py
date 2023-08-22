from flask import Flask, request
from flask_cors import CORS
import time
import json
import bcrypt

from chatbot.assistant.chatbot import Chatbot as AssistantCB
from chatbot.internet.chatbot import Chatbot as InternetCB
from chatbot.intranet.chatbot import Chatbot as IntranetCB

from chatbot.message import Message

app = Flask(__name__)
CORS(app)

# Memory / list of messages
messages = [
    # This list should be filled up by Messages (use Message() to create)
]

# To keep track of when the messages were updated
last_updated = time.time()

# Login details
login = {
    'success': False,
    'login_as': None,   # 'doctor' or 'patient'
    'username': None
}

# Chatbots
doctorbot = AssistantCB('doctor')
patientbot = AssistantCB('patient')
intranetbot = IntranetCB()
internetbot = InternetCB()

# Chat handler
@app.route("/chat", methods=['GET', 'PUT', 'DELETE'])
async def handle_chat():
    global messages
    global login
    global last_updated

    if request.method == 'GET':

        #Check if we want to continue response generation (if we are waiting for function results)
        if messages != [] and messages[-1].get().get('function_call'):
            assistant_message = internetbot.continue_chat()

            messages.append(assistant_message)
            last_updated = time.time()

    # Generate response to query
    elif request.method == 'PUT':
        
        # Information needed in the request:
        request_template = {
            'query': '',            # User query
            'settings': {
                'chatbot_type': '', # Which chatbot, i.e. internet, intranet, doctor or patient
                # Plus any more settings
            }
        }

        # Get all needed information from the request body
        req = request.get_json()

        query = req['query']
        settings = req['settings']

        # Add the query to the conversation
        user_message = Message(role='user', content=query)
        messages.append(user_message)

        # Generate a response to the request
        if settings['chatbot_type'] == 'doctor':
            # Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['doctors'][login['username']]['patients']
            
            assistant_message = doctorbot.get_chat_response(messages=messages, settings=settings, patients=accessible_patients)

        elif settings['chatbot_type'] == 'patient':
            assistant_message = patientbot.get_chat_response(messages=messages, settings=settings, patients=[login['username'][1:]])
        
        elif settings['chatbot_type'] == 'intranet':
            assistant_message = intranetbot.get_chat_response(messages=messages, settings=settings)

        elif settings['chatbot_type'] == 'internet':
            
            #Start process of getting a response
            assistant_message = internetbot.start_chat(messages=messages, settings=settings)
        
        else:
            raise Exception('Incorrect chat_type')


        # Add the new reponse and update the conversation
        messages.append(assistant_message)
        last_updated = time.time()

    # Reset chat
    elif request.method == 'DELETE':
        _reset_chat()

    
    # Returnable conversation, need to change from Message objects to dict, to json
    conversation = {
        'last_updated': last_updated,
        'messages': []
    }
    
    if messages != []:
        for message in messages:
            conversation['messages'].append(message.get())

    return json.dumps(conversation)


# Authentication handler (GET is used to check auth status)
@app.route("/credentials", methods=['GET', 'PUT', 'DELETE'])
async def handle_login():
    global login

    # Attempt login
    if request.method == 'PUT':
        login = {
            'success': False,
            'login_as': None,
            'username': None
        }

        # Get information from the request
        req = request.get_json()
        username = req['username']
        password = req['password']
        login_as = req['login_as'] # This is either 'doctor' or 'patient'

        #Check if credentials exist in the "database"
        with open("credentials/credentials.json") as f:
            users = json.load(f)

            # Find user credentials of the correct type (doctor or patient)
            users = users['credentials'][login_as + 's']
            
            if username in users:
                ref_password = users[username]["password"]
                
                # converting password and reference password to arrays of bytes
                pw_bytes = password.encode('utf-8')
                ref_bytes = ref_password.encode('utf-8')

                if bcrypt.checkpw(pw_bytes, ref_bytes):
                    # Reset chat on login for safety's sake
                    _reset_chat()

                    login["success"] = True
                    login["username"] = username
                    login["login_as"] = login_as
            else:
                login = {
                    'success': False,
                    'login_as': None,
                    'username': None
                }

    # Logout (reset)
    elif request.method == 'DELETE':
        _reset_chat()

        login = {
            'success': False,
            'login_as': None,
            'username': None
        }
    
    return login


def _reset_chat():
    global doctorbot
    global patientbot
    global intranetbot
    global internetbot
    global messages
    global last_updated

    # Reset everything
    doctorbot = AssistantCB('doctor')
    patientbot = AssistantCB('patient')
    intranetbot = IntranetCB()
    internetbot = InternetCB()

    messages = []
    last_updated = time.time()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)