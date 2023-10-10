import datetime
import tm_color

class Console:
    WARNING = f'{tm_color.colors.fg.yellow}[WARNING]:{tm_color.colors.reset}'
    ERROR = f'{tm_color.colors.fg.red}[ERROR]:{tm_color.colors.reset}'

    def getPrefix():
        return f'{tm_color.colors.fg.darkgrey}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{tm_color.colors.reset}'