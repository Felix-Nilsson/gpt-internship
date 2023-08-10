import sys
import os
import openai
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db_doc

from svelte.chatbot.chat_utils import chat_message, frontend_message
from termcolor import colored

from svelte.chatbot.internet.tools import search_1177, search_FASS, search_internetmedicin, get_functions


class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.memory = []
        self.settings = {}


    def get_system_message(self):
        # Path to the system message/system prompt file
        current_script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))
        file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_internet_test.txt')

        # Get the system message from the file
        system_message = ""
        with open(file_path, "r", encoding='utf-8') as f:
            system_message = f.read()
        
        return system_message



    def get_chat_response(self):

        # Get a response from the model
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=self.memory,
            functions=get_functions(),
            function_call='auto',
            temperature=0, #Degree of randomness of the model's output
        )
        # Final response or function call?
        finish_reason = response['choices'][0]['finish_reason']
        
        #TODO use response['usage']['prompt_tokens'] to limit the length of the local memory
        # (How do we keep the conversation in server at a reasonable length?)

        # Assistant wants to call a function
        if finish_reason == 'function_call':
            message = response['choices'][0]['message']
            function_to_call = message['function_call']['name']
            function_arguments = json.loads(message['function_call']['arguments'])
            
            self.memory.append(chat_message(role='assistant', content=None, function_call=message['function_call'], finish_reason='function_call'))
            
            return_thought = f'''{function_arguments['explanation']} \nSök {function_to_call} efter {function_arguments['search_query']}'''

            # Return the last message in the memory
            return chat_message(role='assistant', content=return_thought, function_call=message['function_call'], finish_reason='function_call')

        # Assistant is done
        elif finish_reason == 'stop':
            
            final_response = str(response['choices'][0]['message']['content'])

            # Sources
            sources = []
            
            for message in messages:
                if message['role'] == 'function':
                    sources.append(message)
                elif message["role"] == "assistant" and message.get("function_call"):
                    message['function_call'] = dict(message['function_call'])
                    sources.append(message)


            # Done, return
            return frontend_message(role='assistant', content=final_response, final=True, chat_type='internet', settings=settings, sources=sources)
        
        else:
            raise Exception('Something went wrong :(')


    def start_chat(self, messages: list, settings: dict):
        """Takes a list of messages, returns a Message containing all relevant information.
        (Intranet)
        
        :param messages: The full conversation including the latest query
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)

        :return: Message with all needed information, check message.py in utils for more information.
        """

        # Get the system message!
        #system_message = self.get_system_message()
        
        # Remove unnecessary line
        #system_message = system_message.replace('Du ska svara på följande meddelande "{{input}}".', '')

        # Add relevant data to the query to the system message
        #system_message = system_message.replace('background', str(data))

        
        system_message = f'''Du är en "conversational AI".
        Du svarar på frågor från både läkare och patienter om symtom, sjukdomar, medicin och liknande.
        Du använder bara informationen som du får från de funktioner du har tillgång till.
        Om det är oklart, be om förtydling.'''

        # Reset memory and settings for this message
        self.memory = messages.copy()
        self.settings = settings.copy()

        # Add the system message to the beginning of the messages list
        self.memory.insert(0, chat_message(role='system', content=system_message, function_call=None, finish_reason=None))

        return self.get_chat_response()



    def continue_chat(self):

        if self.memory == []:
            raise Exception('Cannot continue chat! It was never started.')
        
        function_call = self.memory[-1]['function_call']
        function_to_call = function_call['name']
        function_arguments = json.loads(function_call['arguments'])

        search_response = ''

        if function_to_call == '1177':
            search_response = search_1177(function_arguments['search_query'])
        elif function_to_call == 'FASS':
            search_response = search_FASS(function_arguments['search_query'])
        elif function_to_call == 'internetmedicin':
            search_response = search_internetmedicin(function_arguments['search_query'])
        
        self.memory.append(chat_message(role='function', content=str(search_response), function_call=None, finish_reason=None))

        return self.get_chat_response()
        


# Avoid these two, are only to print the conversation
def pretty_print_message(message):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color["system"]))

    elif message["role"] == "user":
        print(colored(f"user: {message['content']}\n", role_to_color["user"]))

    elif message["role"] == "assistant" and message.get("function_call"):

        function_to_call = message['function_call']['name']
        function_arguments = json.loads(message['function_call']['arguments'])
        
        print(colored(f'thought: {function_arguments["explanation"]} \ncall function: {function_to_call}(search_query="{function_arguments["search_query"]}")\n', role_to_color["assistant"]))

    elif message["role"] == "assistant" and not message.get("function_call"):
        print(colored(f"assistant: {message['content']}\n", role_to_color["assistant"]))

    elif message["role"] == "function":
        content = eval(message['content'])
        pretty_sources = json.dumps(content, indent=2)

        print(colored(f"{message['name']}() -> {pretty_sources}\n", role_to_color["function"]))

def pretty_print_conversation(messages):
    for message in messages:
        pretty_print_message(message=message)



test = Chatbot()

test_response = test.get_chat_response([{'role':'user', 'content':'Berätta om borrelia'}], {})