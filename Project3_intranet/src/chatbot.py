import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db.chroma import query_db_doc

class Chatbot:
    def __init__(self):
# ! Do not forget to set the environment variable !
        openai.api_key = os.getenv('OPENAI_API_KEY')

        #Conversation memory
        self.memory = [{'role':'system', 'content': ""}]


    def get_chat_response(self,query: str, remember=True, positive=True, model='gpt-3.5-turbo-0613'):
        """Takes a query and a list of patients whose information the doctor can access, returns a response to the query"""

        #Get patient data related to the query
        data = query_db_doc(query=query,name="docs")
        print(f"heheh {data}")

        #Context/System message to describe what the gpt is supposed to do
        context = f'''
        Du är en AI-assistent som ska svara på frågor.
        Du svarar alltid kort och koncist, inte längre än 2 meningar.
        Säg gärna vilken fil du hittade informationen i.
        Du får endast använda informationen som är avgränsad med tre understreck.
        Använd bara informationen som är avgränsad med tre understreck.
        Om du inte hittar svaret i informationen svarar du att du inte har tillgång till informationen.

        ___{data}___
        '''
        
        
        if not remember:
            #Reset conversation memory
            messages = [{'role':'system', 'content': context}]
        else:
            messages = self.memory
        #Update the context with relevant information for every question
        

        messages[0] = {'role':'system', 'content': context}

        #Add the query to the conversation memory
        messages.append({'role':'user','content':query})

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, #Degree of randomness of the model's output
        )

        #Add the response to the conversation memory
        messages.append({'role':'assistant','content':response.choices[0].message["content"]})

        finished_response = f'''{response.choices[0].message["content"]}'''
        

        #print(status,self.patient_ids)

        return(finished_response)

chatbot = Chatbot()
