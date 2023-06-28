import os
import openai
from embeddings.run_query import return_best_record
import json
import re

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

patient_ids = []

conversation = [{'role':'system', 'content': ""}]


def find_patient_ids(string):
    pattern = r'\d{6}'  # Regular expression pattern to match six digits in a row
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return "NONE"

def get_chat_response(query, patients, model="gpt-3.5-turbo-0613"):
    
    response_message = find_patient_ids(query)

    if response_message != "NONE" and response_message in patients:
        patient_ids.insert(0,response_message)

    print("patient_ids:",patient_ids)

    #CALL GPT WITH THE QUERY AND RELEVANT PATIENT INFORMATION
    patient_data = ""
    if patient_ids != []:
        patient_data = return_best_record(query, patient_ids[0])
        patient_data = " ".join(patient_data[0])

    #context has to be defined here now since the patient_data is added into it rather than the prompt
    context_with_data = f'''
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    
    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
    Ifall det inte finns någon information avgränsad av tre understreck, Svara med "Jag har inte tillräckligt med information"
    ___{patient_data}___
    '''

    messages = conversation

    messages.append({'role':'user','content':query})

    #Update the context with relevant information for every question
    messages[0] = {'role':'system', 'content': context_with_data}


    second_response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )

    messages.append({'role':'assistant','content':second_response.choices[0].message["content"]})

    finished_response = f'''{second_response.choices[0].message["content"]} 
    \n*OBS: som läkare bär du alltid själv ansvaret mot patienten*'''

    return(finished_response)