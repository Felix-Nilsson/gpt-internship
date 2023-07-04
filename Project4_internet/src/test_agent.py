from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI 
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

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")

template="You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

def search(query):
    search = DuckDuckGoSearchRun()
    return search.run(f"{query} site:1177.se")

tool = [Tool(name='1177', func=search, description='Användbar när du vill ha medicinsk information.')]

agent = initialize_agent(tool, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, early_stopping_method="generate")

agent.run("Jag har ont i huvudet, vad borde jag göra?")





