from langchain.agents import Tool, load_tools
from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os

class Chatbot:
    def __init__(self):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

        

        #template="You are a helpful assistant that translates {input_language} to {output_language}."
        #system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        #human_template="{text}"
        #human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        

    def search_1177(self, query):
        search = DuckDuckGoSearchRun()
        return search.run(f"{query} site:1177.se")

    def search_fass(self, query):
        search = DuckDuckGoSearchRun()
        return search.run(f"{query} site:fass.se")

    def search_internetmedicin(self, query):
        search = DuckDuckGoSearchRun()
        return search.run(f"{query} site:verktyg.internetmedicin.se")


    def get_chat_response(self, query):

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        tool = [
             Tool(name='internetmedicin', func=self.search_internetmedicin, 
                  description= """Användbar när du t.ex behöver söka på
                  en ICD kod för en skada eller sjukdom."""
                  ),
             Tool(name='1177', func=self.search_1177,
                   description='Användbar när du vill ha medicinsk \
                   information, såsom information om sjukdomar,    \
                   skador och vården i allmänhet.'
                   ),
             Tool(name='fass', func=self.search_fass, 
                  description= 'Användbar när du vill ha information om \
                  läkemedel, såsom biverkningar, dosering och tillgång.'
                  )
                ]
        #tool = load_tools(tool)

        agent = initialize_agent(tool, 
                                llm=llm, 
                                agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
                                verbose=True, 
                                max_iterations = 4, 
                                early_stopping_method="generate")

        return agent.run(f"Svara på frågan på svenska: '{query}'")




