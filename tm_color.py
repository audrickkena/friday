class colors:
 
     # TODO: ADD more options for colors and text styling
     '''Colors class:reset all colors with colors.reset; two
     sub classes fg for foreground
     and bg for background; use as colors.subclass.colorname.
     i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
     underline, reverse, strike through,
     and invisible work with the main class i.e. colors.bold
     
     - color code copied from: https://www.geeksforgeeks.org/print-colors-python-terminal/'''
     reset = '\033[0m'
     bold = '\033[1m'
     disable = '\033[2m'
     underline = '\033[4m'
     reverse = '\033[7m'
     strikethrough = '\033[9m'
     invisible = '\033[8m'
 
     class fg:
          black = '\033[30m'
          red = '\033[31m'
          green = '\033[32m'
          orange = '\033[33m'
          blue = '\033[34m'
          purple = '\033[35m'
          cyan = '\033[36m'
          lightgrey = '\033[37m'
          darkgrey = '\033[90m'
          lightred = '\033[91m'
          lightgreen = '\033[92m'
          yellow = '\033[93m'
          lightblue = '\033[94m'
          pink = '\033[95m'
          lightcyan = '\033[96m'
     
     class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'