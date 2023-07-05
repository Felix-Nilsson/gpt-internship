from flask import Flask, send_from_directory, request
import random
from chatbot import Chatbot

app = Flask(__name__)

chatbot = Chatbot()

messages = []

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

#@app.route("/response")
#def post_response():
#    return response

# Path for our main Svelte page
@app.route("/input", methods=['GET'])
def handle_input():
    args = request.args
    if len(args) != 0:
        prompt = args.getlist('prompt')[0]
        messages.append(prompt)
        #print(prompt)
        response = chatbot.get_chat_response(prompt)
        messages.append(response)

    return messages[-1]


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


@app.route("/rand")
def hello():
    return str(random.randint(0, 100))


if __name__ == "__main__":
    app.run(debug=True)
