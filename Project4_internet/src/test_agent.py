from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import os

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0)

tools = load_tools(["llm-math"], llm=llm)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("My brother is 20 years old? What is his current age raised to the 0.43 power?")

