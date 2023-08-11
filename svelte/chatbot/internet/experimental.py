import sys
import os
import openai
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from termcolor import colored

from svelte.chatbot.message import Message
from svelte.chatbot.internet.tools import search_1177, search_FASS, search_internetmedicin, get_functions


class Chatbot:
    def __init__(self):
        # ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.memory:list[Message] = [] # List of Messages
        self.settings = {}


    def start_chat(self, messages: list, settings: dict):
        """Takes the current conversation, including the latest query, returns a response
        
        :param messages: The full conversation including the latest query
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)

        :return: Message with all needed information, check message.py for more information.
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
        self.memory.insert(0, Message(role='system', content=system_message))

        if len(self.memory) < 3:
            pretty_print_conversation(self.memory)

        return self._get_chat_response()



    def continue_chat(self):

        if self.memory == []:
            raise Exception('Cannot continue chat! It was never started. (Call start_chat() for each new user query)')
        
        function_call = self.memory[-1].get()['function_call']
        function_to_call = function_call['name']
        function_arguments = function_call['arguments']

        search_response = ''

        if function_to_call == '1177':
            search_response = search_1177(function_arguments['search_query'])
        elif function_to_call == 'FASS':
            search_response = search_FASS(function_arguments['search_query'])
        elif function_to_call == 'internetmedicin':
            search_response = search_internetmedicin(function_arguments['search_query'])
        
        self.memory.append(Message(role='assistant', content='SEARCH_RESULT' + str(search_response), function_call=None))

        # Print the progress
        pretty_print_message(self.memory[-1])

        return self._get_chat_response()
        

    def get_system_message(self):
        # Path to the system message/system prompt file
        current_script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))
        file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_internet_test.txt')

        # Get the system message from the file
        system_message = ""
        with open(file_path, "r", encoding='utf-8') as f:
            system_message = f.read()

        return Message(role='system', content=system_message)


    def _get_chat_response(self):

        messages = []

        for message in self.memory:
            #print(message.openai_format())
            messages.append(message.openai_format())

        

        # Get a response from the model
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            functions=get_functions(),
            function_call='auto',
            temperature=0, #Degree of randomness of the model's output
        )

        # Final response or function call?
        finish_reason = response['choices'][0]['finish_reason']

        #response_message = Message(role='assistant', content=response['choices'][0]['content'])
        #wrapped_response_msg = message_wrapper(message=response_message, chat_type='internet', finish_reason=finish_reason, settings=self.settings)

        
        
        #TODO use response['usage']['prompt_tokens'] to limit the length of the local memory
        # (How do we keep the conversation in server at a reasonable length?)

        # Assistant wants to call a function
        if finish_reason == 'function_call':
            message = response['choices'][0]['message']
            
            ret_message = Message(role='assistant', content=None, function_call=message['function_call'], final=False, chat_type='internet', settings=self.settings)

            # Add the message to the memory, it will be used when continue_chat() is called
            self.memory.append(ret_message)

            # Print the progress
            pretty_print_message(self.memory[-1])
            
            #TODO !!!! FORMAT THE EXPLANATION IN THE FRONTEND !!!!
            #return_thought = f'''{function_arguments['explanation']} \nSök {function_to_call} efter {function_arguments['search_query']}'''

            return ret_message

        # Assistant is done
        elif finish_reason == 'stop':
            
            final_response = str(response['choices'][0]['message']['content'])

            # Sources
            sources = []
            
            for message in self.memory:
                if message.get()['role'] == 'function':
                    sources.append(message)
                elif message.get()["role"] == "assistant" and message.get().get("function_call"):
                    message.get()['function_call'] = dict(message.get()['function_call'])
                    sources.append(message)

            # Done, return
            ret_message = Message(role='assistant', content=final_response, final=True, chat_type='internet', settings=self.settings, sources=sources)
            
            # Print the progress
            pretty_print_message(ret_message)

            return ret_message
        
        else:
            raise Exception('Something went wrong :(')



# Avoid these two, are only to print the conversation
def pretty_print_message(message:Message):

    color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "thought": "cyan",
        "function": "magenta",
    }

    msg = message.get()
    role = msg['role']
    content = str(msg['content'])

    # System message
    if role == 'system':
        print(colored(f"system: {content} \n", color['system']))
        
    # User message
    elif role == 'user':
        print(colored(f"user: {content} \n", color['user']))

    # Assistant message (function call)
    elif role == 'assistant' and msg.get('function_call'):
        function_to_call = msg['function_call']['name']
        search_query = msg['function_call']['arguments']['search_query']
        explanation = msg['function_call']['arguments']['explanation']
        
        print(colored(f'thought: {explanation} \ncall function: {function_to_call}(search_query="{search_query}") \n', color['thought']))

    # Result from search
    elif role == "assistant" and ('SEARCH_RESULT' in content):
        # Some formatting
        content = content.replace('SEARCH_RESULT','')
        content = eval(content)
        pretty_sources = json.dumps(content, indent=2) 

        print(colored(f"function -> {pretty_sources} \n", color["function"]))
    
    # Assistant message (normal)
    elif role == 'assistant':
        print(colored(f"assistant: {content} \n", color['assistant']))

def pretty_print_conversation(messages):
    for message in messages:
        pretty_print_message(message=message)



test = Chatbot()

first_res = test.start_chat([Message(role='user', content='Berätta om borrelia')], {})

if first_res.get().get('function_call'):
    second_res = test.continue_chat()





