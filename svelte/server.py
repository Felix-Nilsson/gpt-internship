from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
import json
import bcrypt

from internet.chatbot import Chatbot as InternetCB
from intranet.chatbot import Chatbot as IntranetCB

app = Flask(__name__)
CORS(app)

chat_type = "internet"

internet_bot = InternetCB()
intranet_bot = IntranetCB()

conversation = {'time': 0, 'messages': [], 'explanations': []}
result = {'success': "False", 'username': "None"}


@app.route("/")
def base():
    return "data transfer '/internet', '/intranet' ..."


# SET/GET THE CHAT TYPE
@app.route("/chat-type", methods=['PUT', 'GET'])
async def chat_type():
    global chat_type

    if request.method == 'PUT':
        print(request.get_json()['type'])
        chat_type = request.get_json()['type']
    
    return chat_type
        



# INTERNET CHATBOT
@app.route("/internet/get", methods=['GET', 'DELETE'])
async def data():
    global conversation
    if request.method == 'DELETE':
        conversation = conversation = {'time': 0, 'messages': [], 'explanations': []}
        #New clean chatbot so its memory is wiped
        global internet_bot
        internet_bot = InternetCB()
    return conversation


@app.route("/internet", methods=['PUT'])
async def post_response():
    global conversation

    #Get the prompt from the PUT body
    prompt = request.get_json()['prompt']
    #Get a response to the prompt
    response, explanation = internet_bot.get_chat_response(prompt)
    #Update the conversation with the new messages and the time the update took place
    conversation['messages'].append(prompt)
    conversation['messages'].append(response)
    conversation['explanations'].append(explanation)
    conversation['time'] = time.time()
    await data()

    return 'OK'



#INTRANET CHATBOT
@app.route("/intranet/get", methods=['GET', 'DELETE'])
async def intranet_data():
    global conversation
    if request.method == 'DELETE':
        conversation = conversation = {'time': 0, 'messages': [], 'explanations': []}
        #New clean chatbot so its memory is wiped
        global intranet_bot
        intranet_bot = InternetCB()
    return conversation



@app.route("/intranet", methods=["PUT"])
async def put_intranet():
    global conversation

    #Get the prompt from the PUT body
    prompt = request.get_json()['prompt']
    #Get a response to the prompt
    response = intranet_bot.get_chat_response(prompt)
    #Update the conversation with the new messages and the time the update took place
    conversation['messages'].append(prompt)
    conversation['messages'].append(response)
    conversation['explanations'].append(response.split("(")[1])
    conversation['time'] = time.time()
    await intranet_data()

    return 'OK'


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




# Path for all the static files (compiled JS/CSS, etc.)
#@app.route("/<path:path>")
#def home(path):
#    return send_from_directory('client/public', path)


#@app.route("/rand")
#def hello():
#    return str(random.randint(0, 100))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
