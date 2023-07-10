from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
from chatbot import Chatbot
import json
import bcrypt

app = Flask(__name__)
CORS(app)

chatbot = Chatbot()
conversation = {'time': 0, 'messages': []}
result = {'success': "False", 'username': "None"}


@app.route("/")
def base():
    return "data transfer '/data'"

@app.route("/data/get", methods=['GET', 'DELETE'])
async def data():
    global conversation
    if request.method == 'DELETE':
        conversation = {'time': 0, 'messages': []}
    return conversation


@app.route("/data", methods=['PUT'])
async def post_response():

    #Get the prompt from the POST body
    prompt = request.get_json()['prompt']
    #Get a response to the prompt
    response = chatbot.get_chat_response(prompt)
    #Update the conversation with the new messages and the time the update took place
    conversation['messages'].append(prompt)
    conversation['messages'].append(response)
    conversation['time'] = time.time()
    await data()

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
