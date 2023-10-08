class MissingValueInSetup(Exception):
    ''' Exception raised when the setup file is missing a required argument
    
    Attributes:
        var_key = name of the variable missing a value in SETUP.json
    '''

    def __init__(self, var_key):
        self.var_key = var_key
        self.message = f'[ERROR]: {{{self.var_key}}} has not been initialised although it is required! Please initialise this value before starting Danki!'
        super().__init__(self.message)

    def getKey(self):
        return self.var_key

class DefaultValueNotRemoved(Exception):
    ''' Exception raised when the default value in setup file for an option is still present when user has updated the option
    
    Attributes:
        var_key = name of the variable that still has the default value in SETUP.json
    '''

    def __init__(self, var_key):
        self.var_key = var_key
        self.message = f'[ERROR]: {{{self.var_key}}} still contains the default value! Please remove this value before starting Danki!'
        super().__init__(self.message)

    def getKey(self, var_key):
        return self.var_key