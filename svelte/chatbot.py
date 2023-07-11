from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from tools import Tool1177, ToolFASS, ToolInternetmedicin

import os

class Chatbot:
    def __init__(self):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    def get_chat_response(self, query):

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        tools = [Tool1177(), ToolFASS(), ToolInternetmedicin()]

        agent = initialize_agent(tools=tools, 
                                llm=llm, 
                                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                verbose=True, 
                                max_iterations = 3, 
                                early_stopping_method="generate")

        return agent.run(f"Svara på frågan på svenska: '{query}'")
        #return agent.run(query)