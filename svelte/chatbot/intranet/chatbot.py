import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db_doc

from ..chat_utils import Message

class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #Conversation memory
        self.memory = [{'role':'system', 'content': ""}]


    def get_chat_response(self,query: str, settings: dict, remember=True, model='gpt-3.5-turbo-0613'):
        """Takes a query, returns a Message containing all relevant information.
        (Intranet)
        
        :param query: The query/prompt.
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)
        :param remember: If the bot should remember the conversation.

        :return: Message with all needed information, check message.py in utils for more information.
        """

        #Adapt language level from settings
        if settings['language_level'] == 'easy':
            language_level_sys_message = 'Du svarar alltid så att ett barn ska kunna förstå, med en snäll ton.'
        elif settings['language_level'] == 'complex':
            language_level_sys_message = 'Du svarar alltid kort och koncist med en formell stil.'
        else: #Anything other than easy or complex => normal (the default)
            language_level_sys_message = 'Du svarar alltid koncist och tydligt, med en konversionell ton'
        
        explanation = f'''Enligt inställningarna ska assistenten svara med språknivå "{settings['language_level']}".'''


        #Get patient data related to the query
        data = query_db_doc(query=query, name="docs")


        # Path to the system message/system prompt file
        current_script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))
        file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_intranet_test.txt')

        # Get the system message from the file
        system_message = ""
        with open(file_path, "r", encoding='utf-8') as f:
            system_message = f.read()

        # Replace unnecessary line with language level setting
        system_message = system_message.replace('Du ska svara på följande meddelande "{{input}}".', language_level_sys_message)
        # Add data relevant to the query to the system message
        system_message = system_message.replace('background', str(data))

        print(system_message)
        
        if remember:
            messages = self.memory
        else:
            # Reset memory
            messages = [{'role':'system', 'content': system_message}]

        
        # Update the system message
        messages[0] = {'role':'system', 'content': system_message}

        # Add the query to the conversation memory
        messages.append({'role':'user','content':query})

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, #Degree of randomness of the model's output
        )

        # Add the response to the conversation memory
        messages.append({'role':'assistant','content':response.choices[0].message["content"]})

        finished_response = f'''{response.choices[0].message["content"]}'''


        return Message(user=False, content=finished_response, explanation=explanation)
