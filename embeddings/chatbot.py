import os
import openai
from run_query import return_best_record

#journal = open("journal.txt","r")
#with open('journal.txt', 'r') as file:
#    journal = file.read().replace('\n', '')

conversation = [{'role':'system', 'content':
                    'Du är en assistent för sjukvårdspersonal som hjälper dem med deras förberedelser \
                    inför möte med en patient. Använd patientens information för att svara på frågorna. \
                    Om patientens information är på engelska, översätt den till svenska och använd det \
                    för att svara. Om du inte kan svara på en fråga utifrån den information som \
                    finns, svara att du inte vet. Svara alltid på svenska.'},
        ]

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model="gpt-3.5-turbo",): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    conversation.append({'role':'user','content':prompt})
    messages = conversation

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    #print(response)
    conversation.append({'role':'assistant','content':response})
    print(conversation)
    return response.choices[0].message["content"]

def get_chat_response(query):
    #sample_input = "Hej, jag vill veta när min patient Johnny Carlson fick diabetes."

    journal = return_best_record(query)[0][0]

    prompt = f"""
    {query}
    ``` 
    Patientens information: ```{journal}```
    """

    response = get_completion(prompt)

    return response


#get_chat_response("Vilken patient är rädd för cyklar?")