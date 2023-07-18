class Message():
    def __init__(self, user: bool, content: str, sources:str = None, explanation:str = None, patient:str = None, alert: str = None):
        """Create a message
        
        :param user: User or AI (True == User, False == AI)     [Required]
        :param content: The message                             [Required]
        :param sources: Sources, web pages or files             [Optional]
        :param explanations: Explanation/Thought process?       [Optional]
        :param patient: The patient discussed in the message    [Optional]
        :param alert: Alert message                             [Optional]
        """

        self.message = {
            'user': user,
            'content': content,
            'sources': sources,
            'explanation': explanation,
            'patient': patient,
            'alert': alert,
        }

    def get(self):
        return self.message
    
    def set(self, user:bool = None, content:str = None, sources:str = None, explanation:str = None, patient:str = None, alert: str = None):

        if user != None:
            self.message['user'] = user
        
        if content != None:
            self.message['content'] = content
        
        if sources != None:
            self.message['sources'] = sources
        
        if explanation != None:
            self.message['explanation'] = explanation
        
        if patient != None:
            self.message['patient'] = patient
        
        if alert != None:
            self.message['alert'] = alert