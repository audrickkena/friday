import datetime
import tm_color

class Console:
    WARNING = f'{tm_color.colors.fg.yellow}[WARNING]:{tm_color.colors.reset}'
    ERROR = f'{tm_color.colors.fg.red}[ERROR]:{tm_color.colors.reset}'
    

    def getPrefix():
        return f'{tm_color.colors.fg.darkgrey}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{tm_color.colors.reset}'
    
class Setup:
    ROLES_END = '_required_roles'

class DiscordOut:
    ERROR = 'Error was raised! Check console for details'
    ISSUE_GITHUB = 'Please contact the admin or raise an issue in github if this is not working properly.'