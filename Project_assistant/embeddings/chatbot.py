import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import openai
#from Project_assistant.embeddings.run_query import return_best_record
import json
import re


from db.chroma import query_db_with_id


class Chatbot:
    def __init__(self,status):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #All patients that have been asked about
        self.patient_ids = []

        self.status = status

        #Conversation memory
        self.memory = [{'role':'system', 'content': ""}]


    def find_patient_id(self,text: str):
        """Searches through text for a 6-digit patient ID"""

        pattern = r'\d{6}'  #Regular expression pattern to match six digits in a row
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return None

    def get_chat_response(self,query: str, patients: list[str], remember=True, model='gpt-3.5-turbo-0613'):
        """Takes a query and a list of patients whose information the doctor can access, returns a response to the query"""
        
        if self.status == "Doctor":
            current_patient_id = self.find_patient_id(query)
        elif self.status == "Patient":
            current_patient_id = patients[0]

        #Check if the patient 'belongs' to the current doctor
        not_accessible_msg  = ""
        if not current_patient_id in patients:
            not_accessible_msg = " Är du säker på att du har tillgång till patienten?"

        if (current_patient_id is not None) and (current_patient_id in patients):
            self.patient_ids.insert(0,current_patient_id)


        #Get patient data related to the query
        patient_data = ""
        if self.patient_ids != []:
            patient_data = query_db_with_id(query=query,id=self.patient_ids[0],name="patientrecords")
            #patient_data = return_best_record(query, self.patient_ids[0])
            patient_data = " ".join(patient_data["documents"][0])

        #Context/System message to describe what the gpt is supposed to do
        context_doctor = f'''
        Du är en AI-assistent för läkare på ett sjukhus.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        
        Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
        Ifall det inte finns någon information avgränsad av tre understreck, Svara med "Jag har inte tillräckligt med information"
        ___{patient_data}___
        '''

        context_patient = f'''
        Du är en AI-assistent för en patient på ett sjukhus.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        Du får använda informationen avgränsad av tre understreck.

        ___{patient_data}___
        '''

        ending_msg = ''

        if self.status == "Doctor":
            context = context_doctor
            ending_msg = f'''{not_accessible_msg}\n*OBS: som läkare bär du alltid själv ansvaret mot patienten*'''

        elif self.status == "Patient":
            context = context_patient

        messages = self.memory

        if not remember:
            #Reset conversation memory
            messages = [{'role':'system', 'content': context}]

        #Update the context with relevant information for every question
        messages[0] = {'role':'system', 'content': context}

        #Add the query to the conversation memory
        messages.append({'role':'user','content':query})

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, #Fegree of randomness of the model's output
        )

        #Add the response to the conversation memory
        messages.append({'role':'assistant','content':response.choices[0].message["content"]})


        finished_response = f'''{response.choices[0].message["content"]}\n\n{ending_msg}'''

        #print(status,self.patient_ids)

        return(finished_response)

