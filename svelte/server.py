from flask import Flask, send_from_directory, request
from flask_cors import CORS
import time
from chatbot import Chatbot

app = Flask(__name__)
CORS(app)

chatbot = Chatbot()

conversation = {'time': 0, 'messages': []}


@app.route("/")
def base():
    return "data transfer '/data'"

@app.route("/data/get", methods=['GET'])
async def data():
    return conversation

#Svelte will go to /data?q='query', here (server.py) we take that query, get a chat response to it, and post the response to /data
@app.route("/data", methods=['POST'])
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


# Path for all the static files (compiled JS/CSS, etc.)
#@app.route("/<path:path>")
#def home(path):
#    return send_from_directory('client/public', path)


#@app.route("/rand")
#def hello():
#    return str(random.randint(0, 100))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
