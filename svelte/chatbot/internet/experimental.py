import sys
import os
import openai
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db_doc

from svelte.chatbot.chat_utils import Message
from termcolor import colored

from svelte.chatbot.internet.tools import search_1177, search_FASS, search_internetmedicin


class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')


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



    def get_chat_response(self, messages: list, settings: dict, remember=True, model='gpt-3.5-turbo-0613'):
        """Takes a list of messages, returns a Message containing all relevant information.
        (Intranet)
        
        :param messages: The full conversation including the latest query
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)
        :param remember: If the bot should remember the conversation.
        :param model: Model to be used

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
        

        # This is used as a parameter to the functions and asks gpt to provide reasoning for the choice of function and search term.
        explanation_param = {
            'type': 'string',
            'description': 'Detaljerad beskrivning av tankegången från användarens fråga till varför funktionen bör kallas.'
        }

        functions = [
            {
                'name': '1177',
                'description': 'Använd detta verktyg när du behöver svara på frågor om sjukdomar eller skador.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'search_query': {
                        'type': 'string',
                        'description': 'Sökord för att hitta information om, till exempel, en sjukdom eller en skada.'
                        },
                        'explanation': explanation_param
                    },
                    'required': ['search_query', 'explanation']
                }
            },
            {
                'name': 'FASS',
                'description': 'Använd detta verktyg när du behöver svara på frågor om läkermedel, till exempel biverkningar, dosering eller tillgång.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'search_query': {
                            'type': 'string',
                            'description': 'Sökord för att hitta information om, till exempel, läkemedel.'
                        },
                        'explanation': explanation_param
                    },
                    'required': ['search_query', 'explanation']
                }
            },
            {
                'name': 'internetmedicin',
                'description': 'Använd detta verktyg när du behöver information om ICD-koder för skador eller sjukdomar.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'search_query': {
                            'type': 'string',
                            'description': 'ICD-kod.'
                        },
                        'explanation': explanation_param
                    },
                    'required': ['search_query', 'explanation']
                }
            }
        ]

        # Add the system message to the beginning of the messages list, (should be enough with the insert row)
        if messages[0]['role'] != 'system':
            messages.insert(0, {'role':'system', 'content': system_message})
        else:
            messages[0] = {'role':'system', 'content': system_message}

        # Print the conversation up until now
        pretty_print_conversation(messages=messages)

        max_iterations = 10
        for i in range(0,max_iterations):

            # Get a response from the model
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=functions,
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

                messages.append(
                    {
                        'role': 'assistant', 
                        'content': None,
                        'function_call': message['function_call']
                    }
                )
                
                # Print the conversation in beautiful colors
                pretty_print_message(messages[-1])

                search_response = ''

                if function_to_call == '1177':
                    search_response = search_1177(function_arguments['search_query'])
                elif function_to_call == 'FASS':
                    search_response = search_FASS(function_arguments['search_query'])
                elif function_to_call == 'internetmedicin':
                    search_response = search_internetmedicin(function_arguments['search_query'])
                
                messages.append({'role': 'function', 'name': function_to_call, 'content': str(search_response)})
                
                # Print the conversation in beautiful colors
                pretty_print_message(messages[-1])

                # Continue the loop
                continue
                
            # Assistant is done
            elif finish_reason == 'stop':
                
                final_response = str(response['choices'][0]['message']['content'])

                messages.append({'role': 'assistant', 'content': final_response})
                
                # Print the conversation in beautiful colors
                pretty_print_message(messages[-1])

                #for message in messages:
                    #print(message, '\n')

                # Sources
                sources = []
                
                for message in messages:
                    if message['role'] == 'function':
                        sources.append(message)
                    elif message["role"] == "assistant" and message.get("function_call"):
                        message['function_call'] = dict(message['function_call'])
                        sources.append(message)


                # Done, return
                return Message(role='assistant', content=final_response, chat_type='internet', settings=settings, sources=sources)
            
            else:
                raise Exception('Something went wrong :(')




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