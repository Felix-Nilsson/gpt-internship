import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db_doc

from svelte.chatbot.message import Message

class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')



    def get_system_message(self):
        # Path to the system message/system prompt file
        current_script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))
        file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_intranet_test.txt')

        # Get the system message from the file
        system_message = ""
        with open(file_path, "r", encoding='utf-8') as f:
            system_message = f.read()
        
        return system_message


    def get_settings_system_message(self, settings):
        # Adapt language level from settings
        if settings['language_level'] == 'easy':
            return 'Du svarar alltid så att ett barn ska kunna förstå, med en snäll ton.'
        elif settings['language_level'] == 'complex':
            return 'Du svarar alltid kort och koncist med en formell stil.'
        else: #Anything other than easy or complex => normal (the default)
            return 'Du svarar alltid koncist och tydligt, med en konversionell ton'


    def get_chat_response(self, messages: list, settings: dict, model='gpt-3.5-turbo-0613'):
        """Takes a list of messages, returns a Message containing all relevant information.
        (Intranet)
        
        :param messages: The full conversation including the latest query
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)
        :param remember: If the bot should remember the conversation.
        :param model: Model to be used

        :return: Message with all needed information, check message.py in utils for more information.
        """

        # Get the system message!
        system_message = self.get_system_message()
        

        # Language level string to be added to the system message
        language_level_sys_message = self.get_settings_system_message(settings)

        # Replace unnecessary line with language level setting
        system_message = system_message.replace('Du ska svara på följande meddelande "{{input}}".', language_level_sys_message)


        # Get data related to the query
        data = query_db_doc(query=messages[-1]['content'], name="docs")

        # Add relevant data to the query to the system message
        system_message = system_message.replace('background', str(data))
        
        # Create local instance of memory and set system message (with relevant information for the question)
        memory = messages.copy()
        memory.insert(0, Message(role='system', content=system_message))


        # Get a response from the model
        response = openai.ChatCompletion.create(
            model=model,
            messages=memory,
            temperature=0, #Degree of randomness of the model's output
        )

        # Setup for the final Message object
        final_response = response.choices[0].message['content']
        explanation = f'''Enligt inställningarna ska assistenten svara med språknivå "{settings['language_level']}".'''

        return Message(
            role='assistant',
            content=final_response,
            final=True,
            chat_type='intranet',
            settings=settings,
            explanation=explanation
        )
    #Message(role='assistant', content=finished_response, explanation=explanation)
