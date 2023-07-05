from flask import Flask, send_from_directory, request
from flask_cors import CORS
import random
from chatbot import Chatbot

app = Flask(__name__)
CORS(app)

chatbot = Chatbot()

messages = ['Just in case']


@app.route("/")
def base():
    return "data transfer '/data'"


#Svelte will go to /data?q='query', here (server.py) we take that query, get a chat response to it, and post the response to /data
@app.route("/data", methods=['POST', 'GET'])
def post_response():

    if request.method == 'GET':
        args = request.args
        if len(args) != 0:
            prompt = args.getlist('prompt')[0]
            messages.append(prompt)
            #print(prompt)
            response = chatbot.get_chat_response(prompt)
            messages.append(response)

    return messages[-1]


# Path for all the static files (compiled JS/CSS, etc.)
#@app.route("/<path:path>")
#def home(path):
#    return send_from_directory('client/public', path)


#@app.route("/rand")
#def hello():
#    return str(random.randint(0, 100))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
