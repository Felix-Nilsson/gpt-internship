import os
import openai
from embeddings.run_query import return_best_record

#journal = open("journal.txt","r")
#with open('journal.txt', 'r') as file:
#    journal = file.read().replace('\n', '')

#Om du inte kan svara på en fråga utifrån den information som \ finns, svara att du inte vet.

conversation = [{'role':'system', 'content':
                    'Du är en assistent för sjukvårdspersonal som hjälper dem med deras förberedelser \
                    inför möte med en patient. Använd patientens information för att svara på frågorna. \
                    Om patientens information är på engelska, översätt den till svenska och använd det \
                    för att svara. Svara alltid på svenska. Svara alltid med två meningar.'},
        ]

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
    #print(journal[0])

    #todo: join with cooler delimiter
    journal = " ".join(journal[0])
    

    prompt = f"""
    {query}
    ``` 
    Patientens information: ```{journal}```
    """

    response = get_completion(prompt)

    return response