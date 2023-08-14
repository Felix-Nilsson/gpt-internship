import sys
import os
import openai
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db

from svelte.chatbot.message import Message

class Chatbot:
    def __init__(self, user_type):
        # ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #All patients that have been asked about
        self.patient_id_memory = []


        self.user_type = user_type

        #Conversation memory - is now kept outside (server.py)
        #self.memory = [{'role':'system', 'content': ''}]



    def find_patient_id(self,text: str):
        """Searches through text for a 6-digit patient ID"""

        pattern = r'\d{6}'  #Regular expression pattern to match six digits in a row
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return None


    def get_system_message(self):
        # Path to the system message/system prompt file
        current_script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))
        
        # Read the correct file
        if self.user_type == 'doctor':
            file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_doctor_test.txt')
        elif self.user_type == 'patient':
            file_path = os.path.join(parent_directory, 'prompts', 'prompts', 'prompt_patient_test.txt')

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


    def get_chat_response(self, messages: list , settings: dict, patients: list[str], model='gpt-3.5-turbo-0613'):
        """Takes a list of messages and a list of patients whose information the doctor can access, returns a response to the last query.
        (Doctor / Patient)

        :param messages: The full conversation including the latest query (as Messages)
        :param settings: Settings for the chatbot (e.g. how complex/formal language the bot should use)
        :param patients: If doctor list of accessible patients, if patient list of only patient ID.
        :param remember: If the bot should remember the conversation.
        :param model: Model to be used

        :return: Message with all needed information, check message.py in utils for more information.
        """

        # The return values
        final_response = ''
        current_patient = None
        source = None
        explanation = None
        alert_message = None

        if self.user_type == 'doctor':
            #Find patient ID in the query
            current_patient = self.find_patient_id(messages[-1].get()['content'])
        
            if current_patient == None:

                if self.patient_id_memory == []: #No ID provided or in memory
                    current_patient = ''
                    source = 'Inga källor har använts'
                    explanation = 'Assistenten kan inte svara på någon fråga om en patient då du varken gav den ett patient-ID eller har frågat om en patient tidigare.'
                else: #No ID provided, get last discussed ID from memory
                    current_patient = self.patient_id_memory[0]
                    source = 'All information kommer från patient ' + current_patient + 's dokument.'
                    explanation = 'Du gav inget patient-ID med denna fråga därför använder assistenten informationen från den patient som diskuterats innan.'

            elif current_patient in patients: #ID provided and access granted
                source = 'All information kommer från patient ' + current_patient + 's dokument.'
                explanation = 'Du gav ett ID och har tillgång till patientens information.'
            
            else: #ID provided, NOT granted access
                alert_message = 'Du har inte tillgång till patient ' + current_patient + 's journal.'
                current_patient = ''
                source = 'Inga källor har använts'
                explanation = 'Du gav ett ID men du har inte tillgång till den patientens information, därför kan inte assistenten svara.'

        elif self.user_type == 'patient':
            #Use the patient's own ID
            current_patient = patients[0]

            #Set the source and explanation for the response
            source = 'All information kommer från din journal.'
            explanation = 'Assistenten utgår alltid från informationen som finns tillgänglig i din egen journal.'

        
        # Get the system message!
        system_message = self.get_system_message()


        # Language level string to be added to the system message
        language_level_sys_message = self.get_settings_system_message(settings)

        # Replace unnecessary line with language level setting
        system_message = system_message.replace('Du ska svara på följande meddelande "{{input}}".', language_level_sys_message)


        # Get patient data related to the query
        patient_data = ''
        if current_patient != '' and current_patient != None:
            patient_data = query_db(query=messages[-1].get()['content'],id=current_patient,name='patientrecords')
            patient_data = ' '.join(patient_data['documents'][0])

        # Update the system message with relevant patient information
        system_message = system_message.replace('background', patient_data)


        # Create local instance of memory and set system message (with relevant information for the question)
        memory = []
        memory.append(Message(role='system', content=system_message).openai_format())
        for message in messages:
            memory.append(message.openai_format())

        # Get a response from the model
        response = openai.ChatCompletion.create(
            model=model,
            messages=memory,
            temperature=0, #Degree of randomness of the model's output
        )
        
        # Set the explanation for the response
        #TODO explanation = thought_process

        final_response = response.choices[0].message['content']

        return Message(
                role='assistant', 
                content=final_response, 
                final=True, 
                chat_type=self.user_type, 
                settings=settings, 
                sources=source, 
                explanation=explanation, 
                patient=current_patient, 
                alert=alert_message
            )
    

