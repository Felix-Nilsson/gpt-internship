import os

from langchain.agents import AgentType
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from .tools import Tool1177, ToolFASS, ToolInternetmedicin

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

    def get_chat_response(self, query, settings):
        """Takes a query and a dictionary containing relevant settings, returns a Message containing all relevant information.
        
        :param query: The query/prompt.
        :param settings: Settings for the chatbot (e.g. What tools it can use or the complexity of the language).

        :return: Message with all needed information, check message.py in utils for more information.
        """

        #Adapt language level from settings
        language_level_sys_message = 'Assistent anpassar alltid sitt svar utefter mottagaren. Mottagare: '

        if settings['language_level'] == 'easy':
            language_level_sys_message += '10-åring'
        elif settings['language_level'] == 'complex':
            language_level_sys_message += 'Läkare'
        else: #Anything other than easy or complex => normal
            language_level_sys_message += 'Vuxen med svenska som modersmål'

        
        #Change accessible tools from settings
        tools = []

        if "1177.se" in settings['chosen_tools']:
            tools.append(Tool1177())
        if "FASS.se" in settings['chosen_tools']:
            tools.append(ToolFASS())
        if "internetmedicin.se" in settings['chosen_tools']:
            tools.append(ToolInternetmedicin())

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
        system_message = f"""Assistent är en 'large language model' skapad för att hjälpa läkare och patienter att hitta information.
        
        Assistent svarar alltid på svenska, oavsett vilket språk användaren använder.

        
        Assistent vet ingenting själv och använder därför alltid bara de verktyg som Assistent har tillgång till.
        Ifall Assistent inte skulle ha tillgång till några verktyg alls, ber Assistent användaren att dubbelkolla inställningarna så att det finns verktyg för Assistent att använda.

        {language_level_sys_message}
        """

        print(system_message)

        new_prompt = agent.agent.create_prompt(
            system_message=system_message,
            tools=tools
        )

        agent.agent.llm_chain.prompt = new_prompt

        output = agent(query)

        response = output['output']

        sources = None
        if len(output['intermediate_steps']) != 0:
            sources = output['intermediate_steps'][0]

        return Message(user=False, content=response, sources=sources)