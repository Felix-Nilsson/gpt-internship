import os
import openai
from embeddings.run_query import return_best_record

#Om du inte kan svara på en fråga utifrån den information som \ finns, svara att du inte vet.


med_advice_classification_context = '''
You are a classification bot.
You provide a single letter answers to wether a question asks for medical advice.
You answer the letter Y if the question is asking for medical advice and the letter N if it is not.
'''

swedish_context = '''
Du är en AI-assistent för läkare.
Du svarar bara på frågor om medicinsk information och terminologi. 
Du svarar bara med fakta, du kan inte ge medicinsk rådgivning.
Du ignorerar patientinformationen avgränsad med #### om läkaren inte specifikt ber om den.
Du utgår alltid ifrån att läkaren vet bäst.
Du svarar kortfattat och tydligt.
Du svarar alltid på svenska.
'''

english_context = '''
You are a medical assistant
Mainly use the information provided to answer.
If you cannot provide an answer based on the information provided, be clear that you are using information from the internet.
Do not make anything up.
Always answer in swedish.
Even if the information is in english, you answer in swedish.
Your answers should be no longer than 2 sentences.
If you did not receive any background information, ask for more informaion.
The background information is delimited by ```.
'''



# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(conversation, prompt, model="gpt-3.5-turbo",): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    temp = conversation.copy()
    temp.append({'role':'user','content':prompt})

    messages = temp #conversation

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    #print(response)
     #prompt = prompt.split("```")[0]
    #print(prompt)
    
    conversation.append({'role':'user','content':prompt})
    conversation.append({'role':'assistant','content':response.choices[0].message["content"]})

    print(conversation[0])
    return response.choices[0].message["content"]

def get_chat_response(query):

    #sample_input = "Hej, jag vill veta när min patient Johnny Carlson fick diabetes."
    journal = return_best_record(query)

    if len([elem for elem in journal[1] if elem > 0.7]) == 0:
        journal = ""
    else:
    #todo: join with cooler delimiter
        journal = " ".join(journal[0])
    
    json_context = f'''
        Based on the provided ##Message##, return a JSON object with the following content: 
        response (with a response to ##Message##, in swedish),
        med_advice (with a one letter classification whether ##Message## asks for medical advice, Y or N),
        pat_info (with a one letter classification whether ##Message## asks for information about a specific patient or multiple patients).

        If ##Message## asks for information about a specific patient or multiple patients, use ####Patient information#### for your answer.
        Patient information: ####{journal}####
        '''
    conversation = [{'role':'system', 'content': json_context}]

    prompt = f"""
    Message: ##{query}##
    """

    response = get_completion(conversation, prompt)

    return response