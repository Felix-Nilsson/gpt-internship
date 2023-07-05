from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun

import os

class Chatbot:
    def __init__(self):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    def search_ddg(self, query):
            search = DuckDuckGoSearchRun()
            return search.run(f"{query} site:1177.se")

    def get_chat_response(self, query):

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        tool = [Tool(name='1177', func=self.search_ddg, description='Användbar när du vill ha medicinsk information.')]

        agent = initialize_agent(tool, 
                                llm=llm, 
                                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                verbose=True, 
                                max_iterations = 3, 
                                early_stopping_method="generate")

        return agent.run(f"Svara på frågan på svenska: '{query}'")





