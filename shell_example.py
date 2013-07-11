import getpass

from shellbuilder.shell import Shell
from shellbuilder.menu import Menu
from shellbuilder.command import Command, QuitCommand
from shellbuilder import constants


class MyShell(Shell):
    def __init__(self):
        Shell.__init__(self)

        self.name = "My Shell"

        # set the header that appears in the top left of the shell
        self.header = """
   ___                _      _       
  / __\__ _ _ __   __| | ___| | __ _ 
 / /  / _` | '_ \ / _` |/ _ \ |/ _` |
/ /__| (_| | | | | (_| |  __/ | (_| |
\____/\__,_|_| |_|\__,_|\___|_|\__,_|
                                     
        """

        # place sticky text on the top right side of the shell
        # you can change this text by calling sticker() from a command
        self.sticker("Welcome, %s" % getpass.getuser())

        # define commands
        hello_world_com = self.build_hello_command()
        named_com = self.build_named_args_command()
        complex_com = self.build_complex_command()
        invalid_com = self.build_invalid_command()
        quit_com = self.build_quit_command()
        # TODO - stickers demo
        # TODO - new menu
        # TODO - builtin commands

        # define menus
        main_menu = Menu('main')
        #menu display title
        main_menu.title = "Main menu"
        # list of Command objects making up menu
        main_menu.commands = [hello_world_com, named_com, complex_com, invalid_com, quit_com]

        # list of menus
        self.menus = [main_menu]
        # default menu
        self.menu = 'main'

        self.put("""
Welcome to Candela, the simple python shell builder.
You can use Candela to build your own shell-based interfaces.
This is especially good for custom offline tools for games or web production.
For example, if your game requires lots of data in a custom XML format, you can
use Candela to easily set up an editor for that data.

This is an instructional shell app that demonstrates the functionality of Candela.
Try any of the commands listed in the menu bar to continue.
        """)

    def build_hello_command(self):
        com = Command('first_command', 'Intro to commands')
        def _run(*args, **kwargs):
            self.put("""
Congratulations, you just invoked your first command in Candela.
This text is being printed from inside a callback function passed to the library
via a Command object.
You can print text to your shell from anywhere in your Shell subclass by calling
self.put().
            """)
            return constants.CHOICE_VALID
        com.run = _run
        return com

    def build_named_args_command(self):
        com = Command('named my_arg <-f filename> [-g othername]', 'Demonstrate arguments')
        def _val(*args, **kwargs):
            success,message = com.default_validate(*args, **kwargs)
            if not success:
                if len(args) == 0 and len(kwargs) == 0:
                    self.put("""
Some commands accept command line arguments.
When creating a command, you specify these arguments with a special (simple) syntax.
For example, this command is called "%s". It accepts both positional and named arguments.

Positional arguments are indicated by a bare word following the command's name
in the command definition.
Named arguments are wrapped in either <> or [], and contain both the argument name
(starting with '-') and a helpful tip about the argument function.
Named arguments with <> are required, those with [] are optional.


Try passing arguments to this command!
                    """ % com.name)
                else:
                    self.put("""
This command requires one unnamed argument followed by a named argument (-f).
Try this:
%s helloworld -f data.txt
                    """ % com.name)
                return (False, message)
            return (success, message)
        com.validate = _val

        def _run(*args, **kwargs):
            self.put("Got arguments:")
            self.put(args)
            self.put(kwargs)
            self.put("Arguments are passed around in a format quite familiar to python:")
            self.put("Positional arguments in a list, named arguments in a dictionary")
            return constants.CHOICE_VALID
        com.run = _run
        return com

    def build_invalid_command(self):
        com = Command('broken', 'Demonstrate invalid command')
        def _run(*args, **kwargs):
            self.put("I will never print")
            return constants.CHOICE_VALID
        com.run = _run

        def _val(*args, **kwargs):
            message = """
You can write custom validation functions for your commands.
A validation function will run before execution of the command.
If the validation returns False, the command is not run.
The default validation function checks for the presence of all required
arguments, but you can override this behavior by setting the Command's validate member.

This is a command that always fails to validate.
            """
            return (False, message)
        com.validate = _val

        return com

    def build_complex_command(self):
        com = Command('cat <-f filename>', 'Demonstrate arbitrary python running')
        def _run(*args, **kwargs):
            self.put("""
Commands can run arbitrary python via a callback. Here's a callback that reads a
file from your local drive and prints it to the shell.
            """)
            return constants.CHOICE_VALID
        com.run = _run
        return com

    def build_quit_command(self):
        quit_com = QuitCommand(self.name)
        quit_com.alias('q')
        return quit_com

    def do_something_complex(self):
        # magic, mystery, arbitrary python code here
        self.put("Missingno")
        return 42


if __name__ == "__main__":
    MyShell().main_loop().end()
