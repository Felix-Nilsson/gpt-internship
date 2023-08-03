import os

from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from .tools import Tool1177, ToolFASS, ToolInternetmedicin

import openai

from ..chat_utils import Message

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

    def get_chat_response(self, query: str, settings: dict):
        """Takes a query and a dictionary containing relevant settings, returns a Message containing all relevant information.
        (Internet)
        
        :param query: The query/prompt.
        :param settings: Settings for the chatbot (e.g. What tools it can use or the complexity of the language).

        :return: Message with all needed information, check message.py in utils for more information.
        """


        #Change accessible tools from settings
        tools = []

        if "1177.se" in settings['chosen_tools']:
            tools.append(Tool1177())
        if "FASS.se" in settings['chosen_tools']:
            tools.append(ToolFASS())
        if "internetmedicin.se" in settings['chosen_tools']:
            tools.append(ToolInternetmedicin())

        explanation = f'''Enligt inställningarna ska assistenten svara med språknivå "{settings['language_level']}" och har tillgång till källorna {settings['chosen_tools']}'''

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

        system_message = ""
        with open("../../../prompts/prompts/prompt_internet_test.txt", "r") as f:
            system_message = f.read()

        print(system_message)

        new_prompt = agent.agent.create_prompt(
            system_message=system_message,
            tools=tools
        )

        agent.agent.llm_chain.prompt = new_prompt

        output = agent(query)

        response = language_adapter(output['output'], settings['language_level']) #output['output'] #Do language_adapter

        sources = None
        if len(output['intermediate_steps']) != 0:
            sources = output['intermediate_steps'][0]

        return Message(user=False, content=response, sources=sources, explanation=explanation)
    


def language_adapter(response, language_level):

    #Adapt language level from settings
    if language_level == 'easy':
        language_level_sys_message = 'Du är en språk-och-tonöversättare. Ditt jobb är att anpassa den texten (avgränsad av ```) du får så att ett barn ska kunna förstå det. Ifall texten är på något annat språk översätter du den till svenska. Ifall texten är längre än 4 meningar kortar du ner den. Du ändrar inga länkar i texten.'
    elif language_level == 'complex':
        language_level_sys_message = 'Du är en språk-tonöversättare. Ditt jobb är att anpassa texten (avgränsad av ```) du får så att en person som är kunnig inom sjukvård kan få den viktiga information på ett kort och koncist sätt. Ifall texten är på något annat språk översätter du den till svenska. Ifall texten är längre än 4 meningar kortar du ner den. Du ändrar inga länkar i texten.'
    else: #Anything other than easy or complex => normal (the default)
        language_level_sys_message = 'Ifall texten är på något annat språk översätter du den till svenska. Ifall texten är längre än 4 meningar kortar du ner den. Du ändrar inga länkar i texten.'

    
    # Setup query 
    query = f'''{language_level_sys_message}
    
    ```{response}```
    '''

    # Get "language level translation"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user','content':query}],
        temperature=0, #Degree of randomness of the model's output
    )

    return str(response.choices[0].message["content"])

