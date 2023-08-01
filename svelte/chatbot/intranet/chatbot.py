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
            language_level_sys_message = 'Du svarar alltid med en trevlig ton och förtydligar allt så att en person som är opåläst om sjukvård ska kunna förstå.'
        
        explanation = f'''Enligt inställningarna ska assistenten svara med språknivå "{settings['language_level']}".'''



        #Get patient data related to the query
        data = query_db_doc(query=query, name="docs")

        #Context/System message to describe what the gpt is supposed to do
        context = f'''
        Du är en AI-assistent som ska svara på frågor.
        Du svarar alltid kortare än 2 meningar.
        {language_level_sys_message}
        Säg gärna vilken fil du hittade informationen i.
        Du får endast använda informationen som är avgränsad med tre understreck.
        Använd bara informationen som är avgränsad med tre understreck.
        Om du inte hittar svaret i informationen svarar du att du inte har tillgång till informationen.

        ___{data}___
        '''
        
        
        if not remember:
            #Reset conversation memory
            messages = [{'role':'system', 'content': context}]
        else:
            messages = self.memory
        #Update the context with relevant information for every question
        

        messages[0] = {'role':'system', 'content': context}

        #Add the query to the conversation memory
        messages.append({'role':'user','content':query})

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, #Degree of randomness of the model's output
        )

        #Add the response to the conversation memory
        messages.append({'role':'assistant','content':response.choices[0].message["content"]})

        finished_response = f'''{response.choices[0].message["content"]}'''

        

        return Message(user=False, content=finished_response, explanation=explanation)
