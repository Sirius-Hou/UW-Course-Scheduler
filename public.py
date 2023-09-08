import re
import pickle
import os
import sys
import time
import threading

from rich import pretty, inspect

from rich import print as rprint

# Set the console theme
pretty.install()

from rich.progress import Progress, track

progress = Progress()


# Create a console object
from rich.console import Console
console = Console()

from rich.markdown import Markdown
from rich.style import Style
from rich.text import Text
from rich.panel import Panel


console_width = os.get_terminal_size().columns
seperate_line = "=" * console_width

import pyautogui










#---------------------------------
### TEXT FORMATTING CODE ###
# RED: \033[31m
# GREEN: \033[32m
# YELLOW: \033[33m
# BLUE: \033[34m
# MAGENTA: \033[35m
# CYAN: \033[36m
# WHITE: \033[37m
# BOLD: \033[1m
# UNDERLINE: \033[4m
# ITALIC: \033[3m
# RESET: \033[0m
#---------------------------------

def print_text(text, options=[]):
    result = ""
    # Add style to the text
    for op in options:
        if op == 'RED':
            result += "\033[31m"
        if op == 'GREEN':
            result += "\033[32m"
        if op == 'YELLOW':
            result += "\033[33m"
        if op == 'BLUE':
            result += "\033[34m"
        if op == 'MAGENTA':
            result += "\033[35m"
        if op == 'CYAN':
            result += "\033[36m"
        if op == 'WHITE':
            result += "\033[37m"
        if op == 'BOLD':
            result += "\033[1m"
        if op == 'UNDERLINE':
            result += "\033[4m"
        if op == 'ITALIC':
            result += "\033[3m"
        if op == 'RESET':
            result += "\033[0m"

    # Reset style at the end of the text
    result += text + "\033[0m"
    print(result)
    return result


def text_style(text, options=[]):
    result = ""
    # Add style to the text
    for op in options:
        if op == 'RED':
            result += "\033[31m"
        if op == 'GREEN':
            result += "\033[32m"
        if op == 'YELLOW':
            result += "\033[33m"
        if op == 'BLUE':
            result += "\033[34m"
        if op == 'MAGENTA':
            result += "\033[35m"
        if op == 'CYAN':
            result += "\033[36m"
        if op == 'WHITE':
            result += "\033[37m"
        if op == 'BOLD':
            result += "\033[1m"
        if op == 'UNDERLINE':
            result += "\033[4m"
        if op == 'ITALIC':
            result += "\033[3m"
        if op == 'RESET':
            result += "\033[0m"

    # Reset style at the end of the text
    result += text + "\033[0m"
    return result