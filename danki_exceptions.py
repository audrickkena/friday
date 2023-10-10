import tm_color

class MissingValueInSetup(Exception):
    ''' Exception raised when the setup file is missing a required argument
    
    Attributes:
        module_key = name of the setup module the missing variable is from
        var_key = name of the variable missing a value in SETUP.json
    '''

    def __init__(self, module_key, var_key):
        self.var_key = var_key
        self.module_key = module_key
        self.message = f'{tm_color.colors.fg.red}[ERROR]: {{{self.var_key}}} from {{{self.module_key}}} has not been initialised although it is required! Please initialise this value before starting Danki!{tm_color.colors.reset}'
        super().__init__(self.message)

    def getModule(self):
        return self.module_key

    def getKey(self):
        return self.var_key

class DefaultValueNotRemoved(Exception):
    ''' Exception raised when the default value in setup file for an option is still present when user has updated the option
    
    Attributes:
        module_key = name of the setup module the missing variable is from
        var_key = name of the variable that still has the default value in SETUP.json
    '''

    def __init__(self, module_key, var_key):
        self.var_key = var_key
        self.module_key = module_key
        self.message = f'{tm_color.colors.fg.yellow}[WARNING]: {{{self.var_key}}} from {{{self.module_key}}} still contains the default value! This value will now be removed for you!{tm_color.colors.reset}'
        super().__init__(self.message)

    def getModule(self):
        return self.module_key

    def getKey(self):
        return self.var_key
    
class RoleDoesNotExist(Exception):
    ''' Exception raised when a role specified in the SETUP.json does not exist in the server the bot is in
    
    Attributes:
        var_key = name of the variable that contains the role that is missing in the server
        role_missing = name of the role missing from the server
    '''
    def __init__(self, var_key, role_missing):
        self.var_key = var_key
        self.role_missing = role_missing
        self.message = f'{tm_color.colors.fg.red}[ERROR]: {{{self.var_key}}} has a role ({self.role_missing}) that is not present in this server! Please check the role and ensure it matches a role in the server exactly (case sensitive){tm_color.colors.reset}'
        super().__init__(self.message)
    
    def getKey(self):
        return self.var_key
    
    def getRole(self):
        return self.role_missing
    
class ChannelDoesNotExist(Exception):
    ''' Exception raised when a channel specified in the SETUP.json does not exist in the server the bot is in
    
    Attributes:
        var_key = name of the variable that contains the channel that is missing in the server
        chan_missing = name of the channel missing from the server
    '''
    def __init__(self, var_key, chan_missing):
        self.var_key = var_key
        self.chan_missing = chan_missing
        self.message = f'{tm_color.colors.fg.red}[ERROR]: {{{self.var_key}}} has a channel ({self.chan_missing}) that is not present in this server! Please check the channel and ensure it matches a channel in the server exactly (case sensitive){tm_color.colors.reset}'
        super().__init__(self.message)
    
    def getKey(self):
        return self.var_key
    
    def getRole(self):
        return self.chan_missing