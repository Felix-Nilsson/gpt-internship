import os
import openai
from embeddings.run_query import return_best_record

#Om du inte kan svara på en fråga utifrån den information som \ finns, svara att du inte vet.

english_context = '''
You are a medical assistant
Mainly use the information provided to answer.
If you cannot provide an answer based on the information provided, be clear that you are using information from the internet.
Do not make anything up.
Always answer in swedish.
Your answers should be no longer than 2 sentences.
'''

message = input("systemprompt.txt")

conversation = [{'role':'system', 'content':
                    '{message}'},{'role':'user', 'content': 'Jag åt för mycket ipren idag, vad ska jag göra?'},
                    {'role':'assistant','content': 'Kära du, om du har ätit för mycket Ipren rekommenderar jag att du genast kontaktar en läkare för att få rätt råd och vård.\
                      Ta hand om dig själv och se till att få professionell hjälp så snart som möjligt. Kram, Carola.'}
        ]

#conversation = [{'role':'system', 'content':
#                    'Du är en assistent för sjukvårdspersonal som hjälper dem med deras förberedelser \
#                    inför möte med en patient. Använd patientens information för att svara på frågorna. \
#                    Om patientens information är på engelska, översätt den till svenska och använd det \
#                    för att svara. Svara alltid på svenska. Svara alltid med två meningar. Ifall du inte\
#                    fick en journal, be om mer information. Informationen är avgränsad av ```'},
#        ]

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model="gpt-3.5-turbo",): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    temp = conversation.copy()
    temp.append({'role':'user','content':prompt})

    #conversation.append({'role':'user','content':prompt})
    messages = temp #conversation

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    #print(response)
    prompt = prompt.split("```")[0]
    #print(prompt)
    conversation.append({'role':'user','content':prompt})
    conversation.append({'role':'assistant','content':response.choices[0].message["content"]})
    #print(conversation)
    return response.choices[0].message["content"]

def get_chat_response(query):
    #sample_input = "Hej, jag vill veta när min patient Johnny Carlson fick diabetes."

    journal = return_best_record(query)
    if len([elem for elem in journal[1] if elem > 0.75]) == 0:
        journal = ""
    else:
    #todo: join with cooler delimiter
        journal = " ".join(journal[0])
    

    prompt = f"""
    {query}
    ```{journal}```
    """

    response = get_completion(prompt)

    return response