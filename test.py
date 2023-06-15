import openai

# Load your API key from an environment variable or secret management service
with open("apikey.txt","r") as file:
    openai.api_key = file.read().rstrip()

chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])