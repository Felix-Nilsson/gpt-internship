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

from chatbot.chat_utils import Message

app = Flask(__name__)
CORS(app)

#Default to internet chatbot
chatbot = InternetCB()

context = {
    'chat_type': 'internet',
    #...
}

conversation = {
    'last_updated': 0,
    'messages': [
        #This list should be filled up by Message elements (the class will construct them correctly)
    ]
}

result = {
    'success': "False", 
    'username': "None"
}


@app.route("/")
def base():
    return 'Sahlgrenska AI Hjälp "backend"'

def _new_chatbot(chat_type):
    global chatbot
    global context
    global conversation

    #New conversation
    conversation = {
        'last_updated': 0,
        'messages': [
            #This list should be filled up by Message elements (the class will construct them correctly)
        ]
    }

    #Set the correct chatbot
    if chat_type == "patient":
        chatbot = AssistantCB("patient")
    elif chat_type == "doctor":
        chatbot = AssistantCB("doctor")
    elif chat_type == "intranet":
        chatbot = IntranetCB()
    else:
        chatbot = InternetCB()
    
    #Reset the context
    context = {
        'chat_type': chat_type,
        #...
    }



# CONTEXT OF THE CHAT
@app.route("/context", methods=['GET', 'PUT'])
async def chat_context():
    global context

    if request.method == 'PUT':
        context['chat_type'] = request.get_json()['chat_type'] 
    
        #Change to chatbot of current type
        _new_chatbot(context['chat_type'])

    return context



@app.route("/chat", methods=['GET', 'PUT', 'DELETE'])
async def chat():
    global chatbot
    global conversation
    
    if request.method == 'PUT':
        #Get the prompt from the PUT body
        prompt = request.get_json()['prompt']


        #Get a response to the prompt
        if context['chat_type'] == 'patient':
            assistant_message = chatbot.get_chat_response(prompt, [result['username'][1:]])
            
        elif context['chat_type'] == 'doctor':
            #Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['doctors'][result['username']]['patients']
            
            assistant_message = chatbot.get_chat_response(prompt, accessible_patients)


        elif context['chat_type'] == 'intranet':
            assistant_message = chatbot.get_chat_response(prompt)

        else: #internet
            assistant_message = chatbot.get_chat_response(prompt)

        #The prompt/query is the same independently of the type of response we want
        user_message = Message(user=True, content=prompt)

        # Add the new messages and update the conversation
        conversation['messages'].append(user_message.get())
        conversation['messages'].append(assistant_message.get())
        conversation['last_updated'] = time.time()
        
    elif request.method == 'DELETE':
        #New chatbot to clear its memory
        _new_chatbot(context['chat_type'])
        conversation['last_updated'] = time.time()

    

    return conversation




@app.route("/credentials", methods=['GET', 'PUT', 'DELETE'])
async def creds():
    global result

    #Attempt login
    if request.method == 'PUT':

        #If the login is not successful, it is unsuccessful, indeed
        result["username"] = None
        result["success"] = False

        #Get username and password from the input
        username = request.get_json()['username']
        candidate_password = request.get_json()['password']

        #Check if credentials exist in the "database"
        with open("credentials/credentials.json") as f:
            users = json.load(f)

            #Chat-type dependant login
            if context['chat_type'] == 'patient':
                users = users['credentials']['patients']
            elif context['chat_type'] == 'doctor' or context['chat_type'] == 'intranet':
                users = users['credentials']['doctors']
            else:
                users = {}
            
            if username in users:
                reference_password = users[username]["password"]
                
                # converting password to array of bytes
                bytes = candidate_password.encode('utf-8')

                if bcrypt.checkpw(bytes,reference_password.encode('utf-8')):
                    result["username"] = username
                    result["success"] = True

    #Logout
    elif request.method == 'DELETE':
        result["username"] = None
        result["success"] = False
    
    return result


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
