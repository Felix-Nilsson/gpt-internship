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
    'conversation': {
        'last_updated': time.time(),
        'messages': [
            # This list should be filled up by Messages (use Message() to create)
        ]
    },
    'login': {
        'success': False,
        'login_as': 'None',     #'doctor' or 'patient'
        'username': 'None'
    }
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
        if combo['conversation']['messages'][-1].get().get('function_call'):
            assistant_message = internetbot.continue_chat()

            combo['conversation']['messages'].append(assistant_message.get())
            combo['conversation']['last_updated'] = time.time()

    # Generate response to query
    elif request.method == 'PUT':
        
        # Information needed in the request:
        request_template = {
            'query': '',        # User query
            'chat_type': '',    # Which chatbot, i.e. internet, intranet, doctor or patient
            'settings': {
                # This includes any settings for the current chat
            }
        }

        # Get all needed information from the request body
        req = request.get_json()
        query = req['query']
        chat_type = req['chat_type']
        settings = req['settings']

        # Add the query to the conversation
        user_message = Message(role='user', content=query)
        combo['conversation']['messages'].append(user_message)

        # Generate a response to the request
        if chat_type == 'doctor':
            assistant_message = doctorbot.get_chat_response(messages=combo['conversation'], settings=settings, patients=[combo['login']['username'][1:]])

        elif chat_type == 'patient':
            # Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['doctors'][combo['login']['username']]['patients']
            
            assistant_message = patientbot.get_chat_response(messages=combo['conversation'], settings=settings, patients=accessible_patients)
        
        elif chat_type == 'intranet':
            assistant_message = intranetbot.get_chat_response(messages=combo['conversation'], settings=settings)

        elif chat_type == 'internet':
            
            #Start process of getting a response
            assistant_message = internetbot.start_chat(messages=combo['conversation'], settings=settings)
        
        else:
            raise Exception('Incorrect chat_type')

        #The prompt/query is the same independently of the type of response we want
        user_message = Message(role='user', content=query)

        # Add the new messages and update the conversation
        combo['conversation']['messages'].append(user_message.get())
        combo['conversation']['messages'].append(assistant_message.get())
        combo['conversation']['last_updated'] = time.time()

    # Reset chat
    elif request.method == 'DELETE':
        pass

    
    return combo['conversation']


# Authentication handler (GET is used to check auth status)
@app.route("/credentials", methods=['GET', 'PUT', 'DELETE'])
async def combo_login():
    global combo

    # Attempt login
    if request.method == 'PUT':

        # Get information from the request
        username = request.get_json()['username']
        password = request.get_json()['password']
        login_as = request.get_json()['login_as'] # This is either 'doctor' or 'patient'

        #Check if credentials exist in the "database"
        with open("credentials/credentials.json") as f:
            users = json.load(f)

            # Find user credentials of the correct type (doctor or patient)
            users = users['credentials']['login_as' + 's']
            
            if username in users:
                ref_password = users[username]["password"]
                
                # converting password and reference password to arrays of bytes
                pw_bytes = password.encode('utf-8')
                ref_bytes = ref_password.encode('utf-8')

                if bcrypt.checkpw(pw_bytes, ref_bytes):
                    combo['login']["success"] = True
                    combo['login']["username"] = username
                    combo['login']["login_as"] = login_as

    # Logout (reset)
    elif request.method == 'DELETE':

        #TODO Reset conversation

        combo['login'] = {
            'success': False,
            'login_as': 'None',
            'username': 'None'
        }

    
    return combo['login']