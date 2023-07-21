import sys
import os
import openai
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from db.chroma import query_db

from ..chat_utils import Message

class Chatbot:
    def __init__(self, user_type):
        # ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #All patients that have been asked about
        self.patient_ids = []


        self.user_type = user_type

        #Conversation memory
        self.memory = [{'role':'system', 'content': ''}]



    def find_patient_id(self,text: str):
        """Searches through text for a 6-digit patient ID"""

        pattern = r'\d{6}'  #Regular expression pattern to match six digits in a row
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return None



    def get_chat_response(self,query: str, patients: list[str], remember=True, model='gpt-3.5-turbo-0613'):
        """Takes a query and a list of patients whose information the doctor can access, returns a Message containing all relevant information.
        
        :param query: The query/prompt.
        :param patients: If doctor list of accessible patients, if patient list of only patient ID.
        :param remember: If the bot should remember the conversation.

        :return: Message with all needed information, check message.py in utils for more information.
        """

        #The return values
        final_response = ''
        current_patient = None
        source = None
        explanation = None
        alert_message = None

        #System messages to describe what the gpt is supposed to do
        sys_message_doctor = f'''
        Du är en AI-assistent för läkare på ett sjukhus.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        
        Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
        Ifall det inte finns någon information avgränsad av tre understreck, Svara med "Jag har inte tillräckligt med information"
        '''

        sys_message_patient = f'''
        Du är en AI-assistent för en patient på ett sjukhus.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        Du får använda informationen avgränsad av tre understreck.
        '''
        
        if self.user_type == 'doctor':
            #Find patient ID in the query
            current_patient = self.find_patient_id(query)
        

            if current_patient == None:

                if self.patient_ids == []: #No ID provided or in memory
                    current_patient = ''
                    source = 'Inga källor har använts'
                    explanation = 'Assistenten kan inte svara på någon fråga om en patient då du varken gav den ett patient-ID eller har frågat om en patient tidigare.'
                else: #No ID provided, get last discussed ID from memory
                    current_patient = self.patient_ids[0]
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

        #Get patient data related to the query
        patient_data = ''
        if current_patient != '' and current_patient != None:
            patient_data = query_db(query=query,id=current_patient,name='patientrecords')
            patient_data = ' '.join(patient_data['documents'][0])

        

        #Update the system message with information depending on user role
        if self.user_type == 'doctor':
            sys_message = f'''{sys_message_doctor} \n ___{patient_data}___'''
        elif self.user_type == 'patient':
            sys_message = f'''{sys_message_patient} \n ___{patient_data}___'''

        #Get the current memory
        messages = self.memory

        if not remember:
            #Reset conversation memory
            messages = [{'role':'system', 'content': sys_message}]

        #Update the system message with relevant information for every question
        messages[0] = {'role':'system', 'content': sys_message}

        #Add the query to the conversation memory
        messages.append({'role':'user','content':query})

        #Get a response from the model
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, #Degree of randomness of the model's output
        )

        #Add the response to the conversation memory
        messages.append({'role':'assistant','content':response.choices[0].message['content']})

        
        #Set the explanation for the response
        #TODO explanation = thought_process

        final_response = response.choices[0].message['content']

        return Message(user=False, content=final_response, sources=source, explanation=explanation, patient=current_patient, alert=alert_message)

