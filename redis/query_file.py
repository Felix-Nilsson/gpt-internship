import os
import openai

#journal = open("journal.txt","r")
with open('journal.txt', 'r') as file:
    journal = file.read().replace('\n', '')


# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{'role':'system', 'content':'Du är en assistent för sjukvårdspersonal som hjälper dem med deras förberedelser inför möte med en patient. Använd patientens information för att svara på frågorna. Om patientens information är på engelska, översätt den till svenska och använd det för att svara. Om du inte kan svara på en fråga utifrån den information som finns, svara att du inte vet.'},
        {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    print(response)
    return response.choices[0].message["content"]



prompt = f"""
Jag ska träffa John Smith idag, vad kan vara bra att tänka på inför besöket?
``` 
Patientens information: ```{journal}```
"""

response = get_completion(prompt)

print(response)