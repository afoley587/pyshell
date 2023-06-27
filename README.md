# Python Basics: Building A Custom Shell

## Motivation
New shells are coming out all of the time, some better than others.
Some have custom commands or features that make them especially
desireable to other shells. What if you wanted to build your own
to do exactly what you and your team needed? Maybe it's a shell with 
all of your DevOps tooling built in to it? Maybe it's a shell that specializes
in parsing web requests? Maybe it's just something else...

Well, python has this really cool built in library which kind of allows
us to do this: [cmd](https://docs.python.org/3/library/cmd.html). Cmd will
allow us to build a really neat interpreter that, when we run it, resembles a shell.
It also has built in support for tab complete, custom prompts, and help on the commands.
All of this saves us a huge amount of typing and work!

The shell we are going to build together is going to run some basic commands, but
it should give you the taste and know-how to expand upon it were you to want to. We will
support 5 commands:

1. A `bye` command which exits the shell. Similar to the bash/zsh/etc. `exit`.
2. An `asciify` command which takes some text as an argument and then prints some ascii
    art for it.
3. An `animated_asciify` command which does something similar to the above but it
    animates it with colors.
4. A `curl2bs4` command which runs curl, loads the response into BeautifulSoup, and 
    prints the prettified version
5. Finally, a `shell` command which runs shell binaries like `ls`, `echo`, etc.

For brevity, we will focus on the usage of the `cmd` module and will only go over
writing a few commands for our shell, but not all 5. An image of the output of 
each command is under the `Running` section, but all the code is on [GitHub]() for
further inspection!

## Implementation
Let's get started with our imports. The most important import in this script
will be `cmd`. It's going to be the base for our shell, handle tab complete,
and handle a lot of the frameworking.

```python
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
```

Let's then look at our class declaration.

```python
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
```

By inheriting from `cmd.Cmd`, our `Sheller` class will be able to handle all
of the shell interactions and all of the niceities we would want from our shell.
When we enter the shell, we will see whatever is represented by the `intro` attribute.
In our case, this is an ascii representation of the word `Sheller`. Each prompt
of the shell will then be configured using the `prompt` attribute. In this case, it will
be the word `Prompt >>` with red text and a green background. Finally, `current_args`
will just hold whatever our last args were. We will get more into that later!

At this point, we will get something like the below:

```shell
 ____  _          _ _           
/ ___|| |__   ___| | | ___ _ __ 
\___ \| '_ \ / _ \ | |/ _ \ '__|
 ___) | | | |  __/ | |  __/ |   
|____/|_| |_|\___|_|_|\___|_|   
                                

Prompt >> 
```

Let's see all of our commands:

```shell
alexanderfoley@ST-253-MacBook-Pro custom-shell % poetry run python pyshell/main.py
 ____  _          _ _           
/ ___|| |__   ___| | | ___ _ __ 
\___ \| '_ \ / _ \ | |/ _ \ '__|
 ___) | | | |  __/ | |  __/ |   
|____/|_| |_|\___|_|_|\___|_|   
                                

Prompt >> ?

Documented commands (type help <topic>):
========================================
animated_asciify  asciify  bye  curl2bs4  help  shell

Prompt >> 
```

Be sure to try out tab complete. Try typing curl and do a double tab - notice
how it will complete the command for you!

Let's write our first command. Let's start simple with the `bye` command:

```python
    def do_bye(self, arg):
        """Standard bye command to close the shell"""
        return True
```

All this will do is exit the shell and end the python process. Pretty much simulating
an `exit` command in bash. Let's disect the method signature - `def do_bye(self, arg):`.
`cmd.Cmd` will turn any method with a `do_` prefix into a shell command. It will
use the docstring as the help message for the command:

```shell
Prompt >> help bye
Standard bye command to close the shell
```

And it will take any strings after the command as an argument to the function. This will
make more sense in our next function, so let's shelf this for now and move on and look 
at the next function:

```python
    def do_asciify(self, arg):
        """Prints a neat ascii banner with the text passed in via
        the user and command line
        """
        self.current_args = arg
        banner = pyfiglet.figlet_format(arg)
        print(banner)
```

This represents our `asciify` command - let's run it to visualize the output:

```shell
Prompt >> asciify this is cool!
 _   _     _       _                       _ _ 
| |_| |__ (_)___  (_)___    ___ ___   ___ | | |
| __| '_ \| / __| | / __|  / __/ _ \ / _ \| | |
| |_| | | | \__ \ | \__ \ | (_| (_) | (_) | |_|
 \__|_| |_|_|___/ |_|___/  \___\___/ \___/|_(_)
                                               

Prompt >> 
```

This is where that `arg` parameter comes in. Whatever string follows the command
is interpreted as a string and passed to the `arg` positional argument. In the above
command, we send this over to a library called `pyfiglet` which turns it into an ascii
representation and then we print it out.

To keep the post brief, these are the only two commands we will walk through line-by-line.
All of the outputs are posted below though, and all code can be found here on [GitHub]()!

## Running

Let's see a demo below of running through the commands:

![](./img/demo.mov)

