import os
import openai
from embeddings.run_query import return_best_record


f1 = open('Project2_patassist/embeddings/systemprompt.txt', 'r')
message = f1.readlines()
    

conversation = [{'role':'system', 'content':'Din uppgift är att hjälpa en patient med att hålla koll på mediciner, bokningar som kan ses från patientens data. \
                                             Det tredje meddelandet du får är vilken patient du pratar med. \
                                             Svara bara på frågor som handlar om patienten. Ge aldrig medicinsk rådgiving. \
                                             Svara som Carola hade svarat. Svara alltid på svenska. \
                                             Ditt svar ska alltid vara som mest två meningar. \
                                             Du får aldrig ge medicinska råd. \
                                             Patientens data kommer vara avgränsad med ```.'},
                {'role':'user', 'content': 'Jag åt för mycket ipren idag, vad ska jag göra?'},
                {'role':'assistant','content': 'Kära du, om du har ätit för mycket Ipren rekommenderar jag att du genast kontaktar en läkare för att få rätt råd och vård.\
                                                Ta hand om dig själv och se till att få professionell hjälp så snart som möjligt. Kram, Carola.'},
                {'role':'user', 'content': 'Borde jag operera mig?'},
                {'role':'assistant', 'content': 'Kära vän, jag är så tacksam att du vänder dig till mig, men jag måste påminna dig om att jag inte är kvalificerad att ge medicinska råd. Kram!'}
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