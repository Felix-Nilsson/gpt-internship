import os
import openai
from src.similarity import return_best_record
import re

class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #Conversation memory
        self.memory = [{'role':'system', 'content': ""}]


    def get_chat_response(self,query: str, remember=True, model='gpt-3.5-turbo-0613'):
        """Takes a query and a list of patients whose information the doctor can access, returns a response to the query"""

        #Get patient data related to the query
        data = return_best_record(query)
        tmp = ''
        for e in range(len(data[0])):
            tmp += data[0][e]
            tmp += data[1][e]
            tmp += "\n"

        #Context/System message to describe what the gpt is supposed to do
        context = f'''
        Du är en AI-assistent för ett sjukhus.
        Du ska hjälpa personalen med att hitta information från intranätet.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        Säg gärna vilken fil du hittade informationen i.
        Du får använda informationen från intranätet som är avgränsat med tre understreck.

        ___{data}___
        '''


        if not remember:
            #Reset conversation memory
            self.memory = [{'role':'system', 'content': context}]

        #Update the context with relevant information for every question
        self.memory[0] = {'role':'system', 'content': context}

        #Add the query to the conversation memory
        self.memory.append({'role':'user','content':query})

        response = openai.ChatCompletion.create(
            model=model,
            messages=self.memory,
            temperature=0, #Degree of randomness of the model's output
        )

        #Add the response to the conversation memory
        self.memory.append({'role':'assistant','content':response.choices[0].message["content"]})


        finished_response = f'''{response.choices[0].message["content"]}'''

        #print(status,self.patient_ids)

        return(finished_response)
