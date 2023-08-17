from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
import json
import bcrypt
import yaml
from yaml.loader import SafeLoader

from chatbot.assistant.chatbot import Chatbot as AssistantCB
from chatbot.internet.chatbot import Chatbot as InternetCB
from chatbot.intranet.chatbot import Chatbot as IntranetCB

from chatbot.message import Message

app = Flask(__name__)
CORS(app)


combo = {
    'messages': [
        # This list should be filled up by Messages (use Message() to create)
    ],
    'login': {
        'success': False,
        'login_as': None,   #'doctor' or 'patient'
        'username': None
    },
    'last_updated': time.time()
}

doctorbot = AssistantCB('doctor')
patientbot = AssistantCB('patient')
intranetbot = IntranetCB()
internetbot = InternetCB()

# Chat handler
@app.route("/chat", methods=['GET', 'PUT', 'DELETE'])
async def combo_chat():
    global combo

    if request.method == 'GET':

        #Check if we want to continue response generation (if we are waiting for function results)
        if combo['messages'] != [] and combo['messages'][-1].get().get('function_call'):
            assistant_message = internetbot.continue_chat()

            combo['messages'].append(assistant_message)
            combo['last_updated'] = time.time()

    # Generate response to query
    elif request.method == 'PUT':
        
        # Information needed in the request:
        request_template = {
            'query': '',        # User query
            'settings': {
                'chatbot_type': '',# Which chatbot, i.e. internet, intranet, doctor or patient
                # This includes any settings for the current chat
            }
        }

        # Get all needed information from the request body
        req = request.get_json()

        query = req['query']
        settings = req['settings']

        # Add the query to the conversation
        user_message = Message(role='user', content=query)
        combo['messages'].append(user_message)

        # Generate a response to the request
        if settings['chatbot_type'] == 'doctor':
            # Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['doctors'][combo['login']['username']]['patients']
            
            assistant_message = doctorbot.get_chat_response(messages=combo['messages'], settings=settings, patients=accessible_patients)

        elif settings['chatbot_type'] == 'patient':
            assistant_message = patientbot.get_chat_response(messages=combo['messages'], settings=settings, patients=[combo['login']['username'][1:]])
        
        elif settings['chatbot_type'] == 'intranet':
            assistant_message = intranetbot.get_chat_response(messages=combo['messages'], settings=settings)

        elif settings['chatbot_type'] == 'internet':
            
            #Start process of getting a response
            assistant_message = internetbot.start_chat(messages=combo['messages'], settings=settings)
        
        else:
            raise Exception('Incorrect chat_type')


        # Add the new reponse and update the conversation
        combo['messages'].append(assistant_message)
        combo['last_updated'] = time.time()

    # Reset chat
    elif request.method == 'DELETE':
        _reset_chat()

    
    # Returnable conversation, need to change from Message objects to dict/json
    conversation = {
        'last_updated': combo['last_updated'],
        'messages': []
    }
    
    if combo['messages'] != []:
        for message in combo['messages']:
            conversation['messages'].append(message.get())

    return json.dumps(conversation)


# Authentication handler (GET is used to check auth status)
@app.route("/credentials", methods=['GET', 'PUT', 'DELETE'])
async def combo_login():
    global combo

    # Attempt login
    if request.method == 'PUT':

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

                    combo['login']["success"] = True
                    combo['login']["username"] = username
                    combo['login']["login_as"] = login_as
    

    # Logout (reset)
    elif request.method == 'DELETE':
        _reset_chat()

        combo['login'] = {
            'success': False,
            'login_as': None,
            'username': None
        }
    
    return combo['login']


def _reset_chat():
    global doctorbot
    global patientbot
    global intranetbot
    global internetbot
    global combo

    # Reset everything
    doctorbot = AssistantCB('doctor')
    patientbot = AssistantCB('patient')
    intranetbot = IntranetCB()
    internetbot = InternetCB()

    combo['messages'] = []
    combo['last_updated'] = time.time()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)