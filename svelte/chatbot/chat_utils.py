class Message():
    def __init__(self, role:str, content:str, chat_type:str = None, settings:dict = None, sources:str = None, explanation:str = None, patient:str = None, alert:str = None):
        """Create a message
        
        :param role: 'user' or 'assistant'                      [Required]
        :param content: The message                             [Required]
        :param chat_type: Choice of chatbot                     [Optional]
        :param settings: Settings for the message               [Optional]
        :param sources: Sources, web pages or files             [Optional]
        :param explanations: Explanation/Thought process?       [Optional]
        :param patient: The patient discussed in the message    [Optional]
        :param alert: Alert message                             [Optional]
        """

        self.message = {
            'role': role,
            'content': content,
            'chat_type': chat_type,
            'settings': settings,
            'sources': sources,
            'explanation': explanation,
            'patient': patient,
            'alert': alert,
        }

    def get(self):
        return self.message
    
    def set(self, role:str = None, content:str = None, chat_type:str = None, settings:dict = None, sources:str = None, explanation:str = None, patient:str = None, alert: str = None):

        if role != None:
            self.message['role'] = role
        
        if content != None:
            self.message['content'] = content

        if chat_type != None:
            self.message['chat_type'] = chat_type

        if settings != None:
            self.message['settings'] = settings
        
        if sources != None:
            self.message['sources'] = sources
        
        if explanation != None:
            self.message['explanation'] = explanation
        
        if patient != None:
            self.message['patient'] = patient
        
        if alert != None:
            self.message['alert'] = alert