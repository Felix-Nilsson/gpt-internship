from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

import os

class Chatbot:
    def __init__(self):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    def search_1177(self, query):
        search = DuckDuckGoSearchResults()
        return search.run(f"{query} site:1177.se")

    def search_fass(self, query):
        search = DuckDuckGoSearchResults()
        return search.run(f"{query} site:fass.se")

    def search_internetmedicin(self, query):
        search = DuckDuckGoSearchResults()
        return search.run(f"{query} site:verktyg.internetmedicin.se")

    def get_chat_response(self, query):

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        tools = [
            Tool(name='1177', func=self.search_1177, description='Användbar när du behöver information om sjukdomar.'),
            Tool(name='fass', func=self.search_fass, description='Användbar när du behöver information om läkemedel.'),
            Tool(name='internetmedicin', func=self.search_internetmedicin, description='Användbar när du behöver information om ICD-koder.'),
        ]

        agent = initialize_agent(tools=tools, 
                                llm=llm, 
                                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                verbose=True, 
                                max_iterations = 3, 
                                early_stopping_method="generate")

        return agent.run(f"Svara på frågan på svenska: '{query}'")
