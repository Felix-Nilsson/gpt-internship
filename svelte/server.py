from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
import json
import bcrypt
import yaml
from yaml.loader import SafeLoader

from chatbot.assistent.chatbot import Chatbot as AssistantCB
from chatbot.internet.chatbot import Chatbot as InternetCB
from chatbot.intranet.chatbot import Chatbot as IntranetCB

app = Flask(__name__)
CORS(app)

context = {
    'chat_type': 'internet',
    #...
}

chatbot = InternetCB()

#conversation = {'time': 0, 'messages': [], 'explanations': []}

conversation = {
    'last_updated': 0,
    'messages': [
        #This list should be filled up by Message elements (the class will construct them correctly)
    ]
}

class Message():
    def __init__(self, user: bool, content: str, sources:str = None, explanation:str = None, patient:str = None, alert: str = None):
        """Create a message
        
        :param user: User or AI (True == User, False == AI)     [Required]
        :param content: The message                             [Required]
        :param sources: Sources, web pages or files             [Optional]
        :param explanations: Explanation/Thought process?       [Optional]
        :param patient: The patient discussed in the message    [Optional]
        :param alert: Alert message                             [Optional]
        """

        self.message = {
            'user': user,
            'content': content,
            'sources': sources,
            'explanation': explanation,
            'patient': patient,
            'alert': alert,
        }

    def get(self):
        return self.message
    
    def set(self, user:bool = None, content:str = None, sources:str = None, explanation:str = None, patient:str = None, alert: str = None):

        if user != None:
            self.message['user'] = user
        
        if content != None:
            self.message['content'] = content
        
        if sources != None:
            self.message['sources'] = sources
        
        if explanation != None:
            self.message['explanation'] = explanation
        
        if patient != None:
            self.message['patient'] = patient
        
        if alert != None:
            self.message['alert'] = alert





result = {'success': "False", 'username': "None"}


@app.route("/")
def base():
    return 'Sahlgrenska AI Hjälp "backend"'

def _new_chatbot(chat_type):
    global chatbot
    global conversation
    global context

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
            pat_response, pat_current_patient, pat_explanation, pat_alert_message = chatbot.get_chat_response(prompt, [result['username'][1:]])

            new_response = Message(user=False, content=pat_response, explanation=pat_explanation, patient=pat_current_patient, alert=pat_alert_message).get()
            
        elif context['chat_type'] == 'doctor':
            #Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['usernames'][result['username']]['patients']
            
            doc_response, doc_current_patient, doc_explanation, doc_alert_message = chatbot.get_chat_response(prompt, accessible_patients)

            new_response = Message(user=False, content=doc_response, explanation=doc_explanation, patient=doc_current_patient, alert=doc_alert_message).get()

        else: #Intranet or Internet
            response, sources = chatbot.get_chat_response(prompt)

            new_response = Message(user=False, content=response, sources=sources).get()
        

        #The prompt/query is the same independently of the type of response we want
        new_query = Message(user=True, content=prompt).get()

        # Add the new messages and update the conversation
        conversation['messages'].append(new_query)
        conversation['messages'].append(new_response)
        conversation['last_updated'] = time.time()
        
    elif request.method == 'DELETE':
        #New chatbot to clear its memory
        _new_chatbot(context['chat_type'])
    

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
