from flask import Flask, request
from flask_cors import CORS
import time
import json
import bcrypt

from chatbot.assistant.chatbot import Chatbot as AssistantCB
from chatbot.internet.chatbot import Chatbot as InternetCB
from chatbot.intranet.chatbot import Chatbot as IntranetCB

from chatbot.message import Message, dict_to_Message

app = Flask(__name__)
CORS(app)

# Memory / list of messages
all_chats = []
chat_id = 0

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
    global all_chats
    global chat_id
    global login
    global last_updated

    if request.method == 'GET':

        #Check if we want to continue response generation (if we are waiting for function results)
        if all_chats != [] and all_chats[chat_id] != [] and all_chats[chat_id][-1].get().get('function_call'):
            assistant_message = internetbot.continue_chat()

            all_chats[chat_id].append(assistant_message)
            last_updated = time.time()

    # Generate response to query
    elif request.method == 'PUT':
        
        # How the request from the frontend should look:
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
        user_message = Message(role='user', content=query, final=True)
        all_chats[chat_id].append(user_message)

        # Generate a response to the request
        if settings['chatbot_type'] == 'doctor':
            # Get list of the doctor's patients
            with open("credentials/credentials.json") as f:
                users = json.load(f)
                accessible_patients = users['credentials']['doctors'][login['username']]['patients']
            
            # Generate doctor's assistant response
            assistant_message = doctorbot.get_chat_response(messages=all_chats[chat_id], settings=settings, patients=accessible_patients)

        elif settings['chatbot_type'] == 'patient':
            #Generate patient assistant response
            assistant_message = patientbot.get_chat_response(messages=all_chats[chat_id], settings=settings, patients=[login['username'][1:]])
        
        elif settings['chatbot_type'] == 'intranet':
            #Generate intranet assistant response
            assistant_message = intranetbot.get_chat_response(messages=all_chats[chat_id], settings=settings)

        elif settings['chatbot_type'] == 'internet':
            
            #Start process of getting an internet assistant response
            assistant_message = internetbot.start_chat(messages=all_chats[chat_id], settings=settings)
        
        else:
            raise Exception('Incorrect chat_type')

        # Add the new reponse and update the conversation
        all_chats[chat_id].append(assistant_message)
        last_updated = time.time()

    
    # Returnable conversation, need to change from Message objects to dict, to json
    conversation = {
        'last_updated': last_updated,
        'messages': []
    }

    if all_chats[chat_id] != []:
        for message in all_chats[chat_id]:
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
                    # Successful login
                    login["success"] = True
                    login["username"] = username
                    login["login_as"] = login_as
                    return login
            
        # Not successful login
        login = {
            'success': False,
            'login_as': None,
            'username': None
        }

    # Logout (reset)
    elif request.method == 'DELETE':
        # Save chat history to file
        username = login['username']

        with open(f"chat_histories/{username}.json", "w", encoding='utf-8') as f:

            save_chats = {} #{'0': ['chat with index'], '1': ['chat with index 1']}

            if all_chats != []:
                for i in range(len(all_chats)):
                    temp_chat = []
                    for message in all_chats[i]:
                        temp_chat.append(message.get())
                    save_chats[i] = temp_chat.copy()

            json.dump(save_chats, fp=f, indent=4, ensure_ascii=False)

        _reset_chat()
        login = {
            'success': False,
            'login_as': None,
            'username': None
        }
    
    return login

@app.route("/all-chats", methods=['GET', 'POST', 'PUT', 'PATCH'])
async def handle_all_chats():
    global all_chats
    global chat_id

    if request.method == 'GET':

        if all_chats == []:
            # First time setup (on login)
            username = login['username']

            # Read chat history from file
            with open(f"chat_histories/{username}.json", "r", encoding='utf-8') as f:
                json_data = f.read()
                # Check if empty
                if json_data:

                    temp_dict = json.loads(json_data)
                    chat_history = [[]] * len(temp_dict)

                    for i in range(len(temp_dict)):
                        temp_chat = temp_dict[str(i)].copy()
                        
                        for j in range(len(temp_chat)):
                            temp_chat[j] = dict_to_Message(temp_dict[str(i)].copy()[j])
                        
                        chat_history[i] = temp_chat
            
                    all_chats = chat_history.copy()

                else:
                    all_chats = [[]]
            # Set the current chat to the most recent
            chat_id = 0

    # CREATE NEW CHAT
    elif request.method == 'POST':
        all_chats.insert(0, [])
        chat_id = 0

    # CHANGE CURRENT CHAT
    elif request.method == 'PUT':
        req = request.get_json()
        chat_id = int(req['new_id'])

    # DELETE SPECIFIC CHAT
    elif request.method == 'PATCH':
        req = request.get_json()
        delete_id = req['delete_id']

        all_chats.pop(delete_id)

        # Deleted the active chat, move current chat to the lastest
        if delete_id == chat_id:
            chat_id = 0

        # Deleted the last chat, automatically create a new one
        if all_chats == []:
            all_chats.insert(0, [])
            chat_id = 0

        

    # List of titles for the different chats
    titles = []

    if all_chats != []:
        for i in range(len(all_chats)):
            if all_chats[i] != []:
                titles.append(all_chats[i][0].get()['content'])
            else: 
                titles.append('')

    return titles


def _reset_chat():
    global doctorbot
    global patientbot
    global intranetbot
    global internetbot
    global all_chats
    global chat_id
    global last_updated

    # Reset everything
    doctorbot = AssistantCB('doctor')
    patientbot = AssistantCB('patient')
    intranetbot = IntranetCB()
    internetbot = InternetCB()

    all_chats = []
    chat_id = 0

    last_updated = time.time()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)