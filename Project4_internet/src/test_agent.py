from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import ChatPromptTemplate
import os

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0)

def search(query):
    search = DuckDuckGoSearchRun()
    return search.run(f"{query} site:1177.se")

tool = [Tool(name='wiki', func=search, description='Useful when you want information, current or old.')]

agent = initialize_agent(tool, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, early_stopping_method="generate")

agent.run("Jag har ont i huvudet, vad borde jag göra?")





