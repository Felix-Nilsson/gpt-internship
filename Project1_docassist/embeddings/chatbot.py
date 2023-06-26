import os
import openai
from embeddings.run_query import return_best_record

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")


conversation = [{'role':'system', 'content': ""}]

def get_completion(conversation, prompt, model="gpt-3.5-turbo",): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    conversation.append({'role':'user','content':prompt})
    messages = conversation

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )

    conversation.append({'role':'assistant','content':response.choices[0].message["content"]})

    #Print a overview of the conversation, could maybe be used to save a log
    for dict in conversation:
        print("\n=========  " + dict['role'] + "  =========")
        print(dict['content'].split("___")[0])

    finished_response = f"""{response.choices[0].message["content"]} 
        \n*OBS: som läkare bär du alltid själv ansvaret mot patienten*"""

    return finished_response

def get_chat_response(query):

    patient_data = return_best_record(query)

    """
    if len([elem for elem in patient_data[1] if elem > 0.7]) == 0:
        patient_data = ""
    else:
    #todo: join with cooler delimiter"""
    
    patient_data = " ".join(patient_data[0])

    #context has to be defined here now since the patient_data is added into it rather than the prompt
    context_with_data = f'''
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    
    
    
    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.

    ___{patient_data}___
    '''

    #Update the context with relevant information for every question
    conversation[0] = {'role':'system', 'content': context_with_data}

    prompt = f"""{query}"""

    response = get_completion(conversation, prompt)

    return response