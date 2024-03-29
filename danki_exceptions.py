import tm_color
import danki_enums

class MissingValueInSetup(Exception):
    ''' Exception raised when the setup file is missing a required argument
    
    Attributes:
        module_key = name of the setup module the missing variable is from
        option_key = name of the option missing a value in SETUP.json
    '''

    def __init__(self, module_key, option_key):
        self.option_key = option_key
        self.module_key = module_key
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.ERROR} {{{self.option_key}}} from {{{self.module_key}}} has not been initialised although it is required! Please initialise this value before starting Danki!{tm_color.colors.reset}'
        super().__init__(self.message)

    def getModule(self):
        return self.module_key

    def getKey(self):
        return self.option_key

class DefaultValueNotRemoved(Exception):
    ''' Exception raised when the default value in setup file for an option is still present when user has updated the option
    
    Attributes:
        module_key = name of the setup module the missing variable is from
        setting_key = whether it is in the required setting or optional setting
        option_key = name of the option that still has the default value in SETUP.json
    '''

    def __init__(self, module_key, setting_key, option_key):
        self.option_key = option_key
        self.module_key = module_key
        self.setting_key = setting_key
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{self.option_key}}} from {{{self.module_key}}} still contains the default value! This value will now be removed for you!'
        super().__init__(self.message)

    def getModule(self):
        return self.module_key
    
    def getSetting(self):
        return self.setting_key

    def getKey(self):
        return self.option_key
    
class RoleDoesNotExist(Exception):
    ''' Exception raised when a role specified in the SETUP.json does not exist in the server the bot is in
    
    Attributes:
        option_key = name of the option that contains the role that is missing in the server
        role_missing = name of the role missing from the server
    '''
    def __init__(self, option_key, role_missing):
        self.option_key = option_key
        self.role_missing = role_missing
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.ERROR} {{{self.option_key}}} has a role ({self.role_missing}) that is not present in this server! Please check the role and ensure it matches a role in the server exactly (case sensitive)'
        super().__init__(self.message)
    
    def getKey(self):
        return self.option_key
    
    def getRole(self):
        return self.role_missing
    
class ChannelDoesNotExist(Exception):
    ''' Exception raised when a channel specified in the SETUP.json does not exist in the server the bot is in
    
    Attributes:
        option_key = name of the option that contains the channel that is missing in the server
        chan_missing = name of the channel missing from the server
    '''
    def __init__(self, option_key, chan_missing):
        self.option_key = option_key
        self.chan_missing = chan_missing
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.ERROR} {{{self.option_key}}} has a channel ({self.chan_missing}) that is not present in this server! Please check the channel and ensure it matches a channel in the server exactly (case sensitive)'
        super().__init__(self.message)
    
    def getKey(self):
        return self.option_key
    
    def getChannel(self):
        return self.chan_missing
    
class MemberMissingRole(Exception):
    ''' Exception raised when a role specified in the SETUP.json does not exist in the server the bot is in
    
    Attributes:
        user = discord.Member of the person who called the command with a missing role
        command_name = name of the command called
        role_missing = role that the user is missing that the command requires
    '''

    def __init__(self, user, command_name, role_missing):
        self.user = user
        self.command_name = command_name
        self.role_missing = role_missing
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{self.user.display_name}}} does not have the role {{{self.role_missing}}} and was unable to use the command {{{self.command_name}}}'
        super().__init__(self.message)

    def getUser(self):
        return self.user
    
    def getCommand(self):
        return self.command_name
    
    def getRole(self):
        return self.role_missing

class DirectoryMissing(Exception):
    ''' Exception raised when directory does not exist
    
    Attributes:
        path = path to the missing directory
    '''
    
    def __init__(self, path):
        self.path = path
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{self.path}}} is not present! Directory needs to be initialised!'
        super().__init__(self.message)
    
    def getPath(self):
        return self.path
    
class FileMissing(Exception):
    ''' Exception raised when a file does not exist
    
    Attributes:
        path = path to the missing file
    
    '''

    def __init__(self, path):
        self.path = path
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{self.path}}} is not present! File needs to be initialised!'
        super().__init__(self.message)
    
    def getPath(self):
        return self.path
    
class UserNotInVoiceChannel(Exception):
    ''' Exception raised when a user runs a command that needs them to be in a voice channel but they are not connected to any voice channel

    Attributes:
        author = [discord.Member] that ran the command
        command = [string] name of the command
    '''

    def __init__(self, author, command):
        self.author = author
        self.command = command
        self.message = f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{self.author.name}}} ran {{{self.command}}} without being in a voice channel!'
        super().__init__(self.message)

    def getAuthor(self):
        return self.author
    
    def getCommand(self):
        return self.command