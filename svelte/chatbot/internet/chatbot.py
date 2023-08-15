import json
import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from svelte.chatbot.message import Message, pretty_print_conversation, pretty_print_message
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
        system_message = self.get_system_message()
        
        # Remove unnecessary lines
        system_message = system_message.replace('Du ska svara på följande meddelande "{{input}}".', '')
        system_message = system_message.replace('background', '')

        
        #system_message = f'''Du är en "conversational AI".
        #Du svarar på frågor från både läkare och patienter om symtom, sjukdomar, medicin och liknande.
        #Du använder bara informationen som du får från de funktioner du har tillgång till.
        #Om det är oklart, be om förtydling.'''

        # Reset memory and settings for this message
        self.memory = messages.copy()
        self.settings = settings.copy()

        # Add the system message to the beginning of the messages list
        self.memory.insert(0, Message(role='system', content=system_message))

        if len(self.memory):
            #Print the system message and the latest query
            pretty_print_conversation([self.memory[0], self.memory[-1]])

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

        return system_message


    def _get_chat_response(self):

        messages = []

        for message in self.memory:
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

        
        #TODO use response['usage']['prompt_tokens'] to limit the length of the local memory
        # (TO ensure that the conversation is kept at a reasonable length to not pass the token limit)

        # Assistant wants to call a function
        if finish_reason == 'function_call':
            message = response['choices'][0]['message']
            
            ret_message = Message(role='assistant', content=None, function_call=message['function_call'], final=False, chat_type='internet', settings=self.settings)

            # Add the message to the memory, it will be used when continue_chat() is called
            self.memory.append(ret_message)

            # Print the progress
            pretty_print_message(self.memory[-1])

            return ret_message

        # Assistant is done
        elif finish_reason == 'stop':
            
            final_response = str(response['choices'][0]['message']['content'])

            # Sources
            sources = []
            
            # If the answer before the final response contains search results (from a function) add to the return message as sources
            if self.memory[-1].get()['role'] == 'assistant':
                content = self.memory[-1].get()['content']
                if content != None and 'SEARCH_RESULT' in content:
                    content = self.memory[-1].get()['content'].replace('SEARCH_RESULT','')
                    content = eval(content)
                    sources = json.dumps(content)

            # Done, return
            ret_message = Message(role='assistant', content=final_response, final=True, chat_type='internet', settings=self.settings, sources=sources)
            
            # Print the progress
            pretty_print_message(ret_message)

            # Reset memory
            self.memory = []

            return ret_message
        
        else:
            raise Exception('Something went wrong :(')