import os
import openai
from embeddings.run_query import return_best_record
import json

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

patient_ids = []

conversation = [{'role':'system', 'content': ""}]

def run_conversation(query, patients, model="gpt-3.5-turbo-0613"):
    
    print(query)
    
    findIDMessages = [{'role':'system', 
                       'content': f"""You are a identification bot, 
                       your job is to retrieve 6 digit numbers from the text delimited by ___, 
                       e.g. 564967 or 138763. 
                       If no 6 digit number can be found, respond \"NONE\"
                       
                        ___{query}___
                       
                       """}]

    #print(findIDMessages)
    #findIDMessages.append({'role':'user','content':query})

    response = openai.ChatCompletion.create(
        model=model,
        messages=findIDMessages,
    )
    response_message = response["choices"][0]["message"]["content"]

    #findIDMessages.append({'role':'assistant','content':response_message})

    if response_message != "NONE" and response_message in patients:
        #local_id = response_message
        patient_ids.insert(0,response_message)

    #CHECK IF GPT WANTS TO CALL A FUNCTION
    """if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])

        id = function_args.get("id")
        print("Current ID of interest: " + id)"""



    #CALL GPT AGAIN WITH THE NEW INFORMATION
    
    patient_data = ""
    if patient_ids != []:
        patient_data = return_best_record(query, patient_ids[0])
        patient_data = " ".join(patient_data[0])

    #context has to be defined here now since the patient_data is added into it rather than the prompt
    context_with_data = f'''
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    
    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.

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


def get_chat_response(query, patients):

    response = run_conversation(query, patients)

    return response