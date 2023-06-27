# The shell framework
import cmd
# Random integers
from random import randint
# Handles interactions with shell subprocesses
import subprocess

# For ascii animations
from asciimatics.screen import Screen
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
# For parsing web responses and prettifying them
from bs4 import BeautifulSoup
# For colors
from colorama import Fore, Back, Style
# For ascii banners
import pyfiglet

class Sheller(cmd.Cmd):
    """The entrypoint for our shell, inheriting from cmd.Cmd

    This class will handle the frameworking and setup for the shell. 
    It will handle the event loop, tab completing, help menus,
    etc.
    """
    # Give us a cool shell entry
    intro  = pyfiglet.figlet_format("Sheller")

    # Our prompt will have red text, a green background, and then will
    # say "Prompt >>"
    prompt = Fore.RED + Back.GREEN + 'Prompt >>' + Style.RESET_ALL + ' '

    current_args = ""

    def do_bye(self, arg):
        """Standard bye command to close the shell"""
        return True
    
    def do_asciify(self, arg):
        """Prints a neat ascii banner with the text passed in via
        the user and command line
        """
        self.current_args = arg
        banner = pyfiglet.figlet_format(arg)
        print(banner)
    
    def do_animated_asciify(self, arg):
        """Prints a neat ascii banner with the text passed in via
        the user and command line
        """           
        self.current_args = arg 
        Screen.wrapper(self.__animated_callback)

    def do_shell(self, arg):
        """Runs a shell command and then prints the output"""
        self.current_args = arg
        command = arg.split()
        print(self.__run_shell_cmd(command=command))

    def do_curl2bs4(self, arg):
        """Runs a curl command through subprocess, and then it will
        load it up into beautiful soup and prettify the results
        """
        self.current_args = arg
        command = ["curl"] + arg.split()
        raw = self.__run_shell_cmd(command=command)
        print(BeautifulSoup(raw, 'html.parser').prettify())

    def __animated_callback(self, screen, **kwargs):
        effects = [
            Cycle(
                screen,
                FigletText(self.current_args, font='big'),
                int(screen.height / 2 - 8)
            ),
            Stars(screen, 200)
        ]
        screen.play([Scene(effects, 10)])

    def __run_shell_cmd(self, command):
        """Runs a shell command with subprocess and returns the text output"""
        return subprocess.run(command, capture_output=True, text=True).stdout

if __name__ == '__main__':
    Sheller().cmdloop()