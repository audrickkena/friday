class MissingValueInSetup(Exception):
    ''' Exception raised when the setup file is missing a required argument
    
    Attributes:
        var_key = name of the variable missing a value in SETUP.json
        message = explanation of the error
    '''

    def __init__(self, var_key, message='Missing value in SETUP.json! Please ensure that the required variables has a value!'):
        self.var_key = var_key
        self.message = message
        super().__init__(self.message)