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

context = {
    'type': 'internet',
    'access_patients': [],
    'current_patient': "",
    #...
}

chatbot = InternetCB()

conversation = {'time': 0, 'messages': [], 'explanations': []}
result = {'success': "False", 'username': "None"}


@app.route("/")
def base():
    return "data transfer '/internet', '/intranet' ..."

def _new_chatbot(chat_type):
    global chatbot
    global conversation
    global context

    #New conversation
    conversation = {'time': 0, 'messages': [], 'explanations': []}

    #Set the correct chatbot
    if chat_type == "patient":
        chatbot = AssistentCB("patient")
    elif chat_type == "doctor":
        chatbot = AssistentCB("doctor")
    elif chat_type == "intranet":
        chatbot = IntranetCB()
    else:
        chatbot = InternetCB()
    
    #Reset the context
    context = {
    'type': chat_type,
    'access_patients': [],
    'current_patient': "",
    #...
}


# CONTEXT OF THE CHAT
@app.route("/context", methods=['GET', 'PUT'])
async def chat_context():
    global context

    if request.method == 'PUT':
        context['type'] = request.get_json()['type']
    
        #Change to chatbot of current type
        _new_chatbot(context['type'])

    return context



@app.route("/chat", methods=['GET', 'PUT', 'DELETE'])
async def chat():
    global chatbot
    global conversation
    
    if request.method == 'PUT':
        #Get the prompt from the PUT body
        prompt = request.get_json()['prompt']
        #Get a response to the prompt
        if context['type'] == 'patient':
            pat_response = chatbot.get_chat_response(prompt, [result['username'][1:]])
            response = pat_response['response']
            explanation = pat_response['explanation']
            
        elif context['type'] == 'doctor':
            #Get the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)

            context['access_patients'] = users['credentials']['usernames'][result['username']]['patients']
            

            doc_response = chatbot.get_chat_response(prompt, context['access_patients'])
            response = doc_response['response']
            explanation = doc_response['explanation']
            context['current_patient'] = doc_response['current_patient']
        else:
            response, explanation = chatbot.get_chat_response(prompt)
        
        #Update the conversation with the new messages and the time the update took place
        conversation['messages'].append(prompt)
        conversation['messages'].append(response)
        conversation['explanations'].append(explanation)
        conversation['time'] = time.time()
        
    elif request.method == 'DELETE':
        #New chatbot to clear its memory
        _new_chatbot(context['type'])
    
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
