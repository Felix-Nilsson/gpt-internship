import json

class Message():
    def __init__(self, role:str, 
                 content:str, function_call:dict = None, 
                 final:bool = False, chat_type:str = None, 
                 settings:dict = None, sources:list = None, 
                 explanation:str = None, patient:str = None, 
                 alert:str = None):
        """Create a Message
        
        :param role:            Message role, 'system', 'user', 'assistant' or 'function'
        :param content:         Content, e.g. a question, a response or function results
        :param function_call:   Information about function that the assistant wants to call
        
        :param final:           Whether the message is the final response to the user query
        :param chat_type:       Which chatbot generated the response
        :param settings:        Settings that were used to generate the response
        :param sources:         (deprecated? could be retrieved from the function message before a final response)
        :param explanation:     Explanation behind the answer
        :param patient:         ID of patient discussed
        :param alert:           Alert message
        """
        
        self.message = {
            'role': role,
            'content': content,
            'function_call': function_call,

            'additional_info': {
                'final': final,
                'chat_type': chat_type,
                'settings': settings,
                'sources': sources,
                'explanation': explanation,
                'patient': patient,
                'alert': alert
            }
        }

        # Fix the arguments (otherwise they are in some weird OpenAI-dict type)
        if function_call != None and function_call.get('arguments'):
            self.message['function_call']['formatted_arguments'] = json.loads(function_call['arguments'])


    def get_internal(self):
        """Get Message that can be used with OpenAI API
        """
        # OpenAI API is pretty picky
        
        # Cleanup
        message = self.message.copy()

        message.pop('additional_info')

        if message['function_call'] == None:
            message.pop('function_call')

        return message


    def get_external(self):
        """Get Message with additional information"""

        return self.message.copy()
    
    def set(self, role:str = None, 
            content:str = None, function_call:dict = None, 
            final:bool = None, chat_type:str = None, 
            settings:dict = None, sources:list = None, 
            explanation:str = None, patient:str = None, 
            alert:str = None):
        """Set/Change one or many of the values in the Message"""
        
        if role:
            self.message['role'] = role
        if content:
            self.message['content'] = content
        if function_call:
            self.message['function_call'] = function_call
        if final:
            self.message['additional_info']['final'] = final
        if chat_type:
            self.message['additional_info']['chat_type'] = chat_type
        if settings:
            self.message['additional_info']['settings'] = settings
        if sources:
            self.message['additional_info']['sources'] = sources
        if explanation:
            self.message['additional_info']['explanation'] = explanation
        if patient:
            self.message['additional_info']['patient'] = patient
        if alert:
            self.message['additional_info']['alert'] = alert




# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\  MESSAGE TEMPLATES /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

# INTERNAL MESSAGES THAT ARE USED WITH OPENAI API (in messages/memory)
# Question from user
user_msg = {
    'role': 'user',
    'content': '', # Användarens fråga
    'function_call': None
}

# Information from function
function_msg = {
    'role': 'function',
    'content': '', # Information från en sökning på t.ex. 1177
    'function_call': None
}

# Assistant Response
assistant_function_msg = {
    'role': 'assistant',
    'content': '', # Slutgiltigt svar till användarens fråga
    'function_call': None
}

# Function call
assistant_function_msg = {
    'role': 'assistant',
    'content': None,
    'function_call': {
        'name': '1177',
        'arguments': {
            'search_query': '', # Sökord till funktionen
            'explanation': '' # AI-ens förklaring, t.ex. 'Jag behöver veta '
        }
    }
}

#EXTERNAL MESSAGE THAT ARE RETURNED TO THE SERVER?
# Assistant Response
assistant_function_msg = {
    'role': 'assistant',
    'content': '', # Slutgiltigt svar till användarens fråga
    'function_call': None,
    'additional_information': {
        'final': True,      #whether the message is the final, i.e. if we are ready for a new query from the user
        'chat_type': '',    #internet atm
        'settings': {},     #settings that were active for the response generation
        'sources': [],      #all sources ? is kinda stupid since there is no guarantee that they were used
        'explanation': '',  #explanation behind the answer (only used by non-internet chatbots)
        'patient': '',      #the id of the patient discussed, only needed for doctor assistant (and patient assistant, but not as)
        'alert': ''         #if any alert should be raised
    }
}

# Function call
assistant_function_msg = {
    'role': 'assistant',
    'content': None,
    'function_call': {
        'name': '1177',
        'arguments': {
            'search_query': '', # Sökord till funktionen
            'explanation': '' # AI-ens förklaring, t.ex. 'Jag behöver veta '
        }
    },
    'additional_information': {
        'final': True,      #A function_call assistant response is nothing more than an progress update. (we could portray the ai thought process live)
        'chat_type': '',    #internet atm
        'settings': {},     #settings that were active for the response generation
        'sources': [],      #all sources ? is kinda stupid since there is no guarantee that they were used
        'explanation': '',  #explanation behind the answer (only used by non-internet chatbots)
        'patient': '',      #the id of the patient discussed, only needed for doctor assistant (and patient assistant, but not as)
        'alert': ''         #if any alert should be raised
    }
}