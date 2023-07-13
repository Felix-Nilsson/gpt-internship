from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
import json
import bcrypt
import yaml
from yaml.loader import SafeLoader

from chatbot.assistent.chatbot import Chatbot as AssistentCB
from chatbot.internet.chatbot import Chatbot as InternetCB
from chatbot.intranet.chatbot import Chatbot as IntranetCB

app = Flask(__name__)
CORS(app)

chat_type = "internet"

chatbot = InternetCB()

conversation = {'time': 0, 'messages': [], 'explanations': []}
result = {'success': "False", 'username': "None"}


@app.route("/")
def base():
    return "data transfer '/internet', '/intranet' ..."

def _new_chatbot(chat_type):
    global chatbot
    if chat_type == "patient":
        chatbot = AssistentCB("patient")
    elif chat_type == "doctor":
        chatbot = AssistentCB("doctor")
    elif chat_type == "intranet":
        chatbot = IntranetCB()
    else:
        chatbot = InternetCB()


# SET/GET THE CHAT TYPE
@app.route("/chat-type", methods=['PUT'])
async def get_set_chat_type():
    global chat_type
    global chatbot
    global conversation

    chat_type = request.get_json()['type']
    
    #reset the chat
    conversation = {'time': 0, 'messages': [], 'explanations': []}
    _new_chatbot(chat_type)

    return chat_type



@app.route("/chat", methods=['GET', 'PUT', 'DELETE'])
async def chat():
    global chatbot
    global conversation
    
    if request.method == 'PUT':
        #Get the prompt from the PUT body
        prompt = request.get_json()['prompt']
        #Get a response to the prompt
        if chat_type == 'patient':
            response = chatbot.get_chat_response(prompt, [result['username'][1:]])
            explanation = "All info kommer från dina egna dokument"
        elif chat_type == 'doctor':
            with open('../patientrecords/config_joined.yaml', 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
            
            patients = config['credentials']['usernames'][result['username']]['patients']

            response = chatbot.get_chat_response(prompt, patients)
            explanation = "All info kommer från dina egna dokument"
        else:
            response, explanation = chatbot.get_chat_response(prompt)
        #Update the conversation with the new messages and the time the update took place
        conversation['messages'].append(prompt)
        conversation['messages'].append(response)
        conversation['explanations'].append(explanation)
        conversation['time'] = time.time()
        
    elif request.method == 'DELETE':
        conversation = {'time': 0, 'messages': [], 'explanations': []}
        #New chatbot to clear its memory
        _new_chatbot(chat_type)
    
    return conversation




@app.route("/credentials/get", methods=['GET'])
async def get_creds():
    return result

@app.route("/credentials", methods=['POST'])
async def set_creds():

    username = request.get_json()['username']
    candidate_password = request.get_json()['password']

    with open("credentials/credentials.json") as f:
        users = json.load(f)
        
        if username in users["credentials"]["usernames"]:
            reference_password = users["credentials"]["usernames"][username]["password"]
            
            # converting password to array of bytes
            bytes = candidate_password.encode('utf-8')

            if bcrypt.checkpw(bytes,reference_password.encode('utf-8')):
                result["username"] = username
                result["success"] = True
    
            else:
                result["username"] = None
                result["success"] = False
            
        else:
            result["username"] = None
            result["success"] = False

    await get_creds()
    
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
