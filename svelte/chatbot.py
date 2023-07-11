from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from tools import Tool1177, ToolFASS, ToolInternetmedicin

import os

class Chatbot:
    def __init__(self):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            input_key='input',
            output_key='output',
            k=5, #Remember 5 messages back
            return_messages=True
        )

    def get_chat_response(self, query):

        
        tools = [Tool1177(), ToolFASS(), ToolInternetmedicin()]

        agent = initialize_agent(
            tools=tools, 
            llm=self.llm, 
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
            verbose=True, 
            return_intermediate_steps=True,
            max_iterations = 3, 
            early_stopping_method="generate",
            memory=self.conversational_memory
        )

        #Update the context/system message
        context = """Assistent är en 'large language model' skapad för att hjälpa läkare och patienter att hitta information.
        
        Assistent svarar alltid på svenska, oavsett vilket språk användaren använder.

        Assistent är här för att hjälpa till och hittar aldrig på information utanför den som finns i de tillgängliga verktygen.

        Assistent svarar alltid med svar som är formaterade enligt markdown.

        Assistent avslutar alltid svaret med en paragraf 'För mer information kan du besöka:' med en punktlista av alla källor som använts för svaret.
        """

        new_prompt = agent.agent.create_prompt(
            system_message=context,
            tools=tools
        )

        agent.agent.llm_chain.prompt = new_prompt

        output = agent(query)

        response = output['output']

        # Use this one to show the explanation to the user, needs to be reformatted?
        print(output['intermediate_steps'])
        explanation = 'WIP'
        #explanation = output['intermediate_steps'][0]

        #agent_action = explanation[0]
        

        #Do this for each explanation[1][i] to get all the sources for step 1
        #print("\nchatbot.py LINK: " + str(explanation[1][0]['link']))
        #print("\nchatbot.py TITLE: " + str(explanation[1][0]['title']))
        #print("\nchatbot.py SNIPPET: " + str(explanation[1][0]['snippet']))
        

        # This one should only keep track of the 5 latest messages, but can be useful to check that it works
        #history = output['chat_history']

        return response, explanation