import openai

# Load your API key from an environment variable or secret management service
with open("apikey.txt","r") as file:
    openai.api_key = file.read().rstrip()

def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text_to_summarize = """ """

prompt = f"""
Your task is to generate a summary of ...
Summarize the journal delimited with ``` 
Journal: ```{text_to_summarize}```
"""

response = get_completion(prompt)

print(response)