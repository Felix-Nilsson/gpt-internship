import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db_doc

from svelte.chatbot.chat_utils import Message
from termcolor import colored


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
        Om det är oklart, be om förtydling.
        '''
        

        # TODO ADD A PARAMETER WHERE THE ASSISTANT PROVIDES REASONING FOR THE CHOICE OF TOOL AND SEARCH QUERY,
        #       THIS WAY WE SHOULD BE ABLE TO GET A PROPER STEP-BY-STEP EXPLANATION !!!!

        """# TILL EXEMPEL 
        'explanation': {
                        'type': 'string',
                        'description': 'En stegvis beskrivning av assistentens tankegång och val av sökord.'
                        }
        """

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
                        }
                    },
                    'required': ['search_query']
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
                        }
                    },
                    'required': ['search_query']
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
                        }
                    },
                    'required': ['search_query']
                }
            }
        ]

        # Create local instance of memory and set system message (with relevant information for the question)
        memory = [{'role':'system', 'content': system_message}]

        # Add the conversation until now to the memory (should include the latest query)
        if remember:
            for message in messages:
                memory.append({'role': message['role'], 
                               'content': message['content']})

        # Get a response from the model
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            temperature=0, #Degree of randomness of the model's output
        )


        # This instance of memory will not be used anymore so ..
        if response.choices[0].message['content'] != None:
            memory.append({'role': 'assistant', 'content': response.choices[0].message['content']})
        elif response.choices[0].message['function_call'] != None:
            memory.append({'role': 'assistant', 'content': response.choices[0].message['function_call']})
        pretty_print_conversation(memory)


        # TODO - This will need modification so that we only add the last (finished) reponse
        # i.e. we need a loop that goes until the chatbot is happy and has given its final response, then return that

        # Setup for the final Message object
        finished_response = response['choices'][0]['message']

        return Message(role='assistant', content=finished_response)







def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))



test = Chatbot()

test_response = test.get_chat_response([{'role':'user', 'content':'Berätta om borrelia'}], {})

print('FINAL REPONSE: ')
print(test_response.get()['content'])

# TODO, LOOP, CHECK IF RESPONSE IS FUNCTION CALL, CALL THE FUNCTION, PROFIT