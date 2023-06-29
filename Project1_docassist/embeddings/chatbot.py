import os
import openai
from embeddings.run_query import return_best_record
import json
import re

# ! Do not forget to set the environment variable !
openai.api_key = os.getenv('OPENAI_API_KEY')

#All patients that have been asked about
patient_ids = []

#Conversation memory
memory = [{'role':'system', 'content': ""}]


def find_patient_id(text: str):
    """Searches through text for a 6-digit patient ID"""

    pattern = r'\d{6}'  #Regular expression pattern to match six digits in a row
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None

def get_chat_response(query: str, patients: list[str], remember=True, model='gpt-3.5-turbo-0613'):
    """Takes a query and a list of patients whose information the doctor can access, returns a response to the query"""
    
    current_patient_id = find_patient_id(query)

    #Check if the patient 'belongs' to the current doctor
    not_accessible_msg  = ""
    if not current_patient_id in patients:
        not_accessible_msg = " Är du säker på att du har tillgång till patienten?"

    if (current_patient_id is not None) and (current_patient_id in patients):
        patient_ids.insert(0,current_patient_id)


    #Get patient data related to the query
    patient_data = ""
    if patient_ids != []:
        patient_data = return_best_record(query, patient_ids[0])
        patient_data = " ".join(patient_data[0])

    #Context/System message to describe what the gpt is supposed to do
    context_with_data = f'''
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    
    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
    Ifall det inte finns någon information avgränsad av tre understreck, Svara med "Jag har inte tillräckligt med information"
    ___{patient_data}___
    '''
    
    messages = memory

    if not remember:
        #Reset conversation memory
        messages = [{'role':'system', 'content': context_with_data}]

    #Update the context with relevant information for every question
    messages[0] = {'role':'system', 'content': context_with_data}

    #Add the query to the conversation memory
    messages.append({'role':'user','content':query})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, #Fegree of randomness of the model's output
    )

    #Add the response to the conversation memory
    messages.append({'role':'assistant','content':response.choices[0].message["content"]})


    finished_response = f'''{response.choices[0].message["content"]}{not_accessible_msg} 
    \n*OBS: som läkare bär du alltid själv ansvaret mot patienten*'''

    return(finished_response)