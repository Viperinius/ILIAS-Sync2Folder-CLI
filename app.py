# based on https://blog.swdev.ed.ac.uk/2017/04/28/writing-python-command-line-tools-with-cliff/

import os
import sys

from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager

from cliff.show import ShowOne
from cliff.lister import Lister

from iliasHandling import IliasHandling
from getpass import getpass

data = [
    [ 'Journal', 'Publisher', 'Print ISSN', 'Online ISSN' ],
    [ 'Journal of Software', 'Computer Publishings', '0000-0000', '0000-0001' ],
    [ 'Journal of Hardware', 'Computer Publishings', '1111-0000', '1111-0001' ],
    [ 'Software Development Monthly', 'Megacorp', '2222-0000', '2222-0001' ],
    [ 'Hardware Letters', 'XIT University Press', '3333-0000', '3333-0001' ],
]

asciiLogo = '''

 ___ _     ___    _    ____       ____                   ____  _____     _     _           
|_ _| |   |_ _|  / \  / ___|     / ___| _   _ _ __   ___|___ \|  ___|__ | | __| | ___ _ __ 
 | || |    | |  / _ \ \___ \ ____\___ \| | | | '_ \ / __| __) | |_ / _ \| |/ _` |/ _ \ '__|
 | || |___ | | / ___ \ ___) |_____|__) | |_| | | | | (__ / __/|  _| (_) | | (_| |  __/ |   
|___|_____|___/_/   \_\____/     |____/ \__, |_| |_|\___|_____|_|  \___/|_|\__,_|\___|_|   
                                        |___/                                              

===========================================================================================
'''

handler =IliasHandling()

class Sync2Folder(App):
    def __init__(self):
        super().__init__(
            description='Download your ILIAS course files to your local disk automatically',
            version='0.1',
            command_manager=CommandManager('sync2folder'),
            deferred_help=True,
        )
    
    # define what commands are available
    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        self.LOG.info(asciiLogo)

        handler = IliasHandling()

        commands = [Filter, Login, Logout, Select, ]
        for command in commands:
            self.command_manager.add_command(command.__name__.lower(), command)

class Filter(Lister):
    'Display selected columns of data'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--index', action='store_true', help='Use column index numbers instead of names')
        parser.add_argument('column', nargs='+', help='Selected columns to display')
        return parser
    
    def take_action(self, parsed_args):
        if parsed_args.index:
            columns = [int(c) for c in parsed_args.column]
        else:
            columns = [data[0].index(c) for c in parsed_args.column]

        selected = [[d[c] for c in columns] for d in data]
        return (selected[0], selected[1:])

class Login(Command):
    'Login to ILIAS'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('-u', nargs='?', help='Pass a user name instead of interactively asking')
        parser.add_argument('-p', nargs='?', help='Pass a password instead of interactively asking')
        return parser

    def take_action(self, parsed_args):
        if parsed_args.u is not None:
            if parsed_args.p is not None:
                result = handler.iliasLogin(parsed_args.u, parsed_args.p)
                print(handler.loggedIn)
                return
            password = getpass('Enter password: ')
            result = handler.iliasLogin(parsed_args.u, password)
            return
        
        if parsed_args.p is not None:
            user = input('Enter user name: ')
            result = handler.iliasLogin(user, parsed_args.p)
            return

        user = input('Enter user name: ')
        password = getpass('Enter password: ')
        result = handler.iliasLogin(user, password)
        return

class Logout(Command):
    'Logout from ILIAS'

    def take_action(self, parsed_args):
        print(handler.loggedIn)
        if handler.loggedIn:
            result = handler.iliasLogout()

class Select(ShowOne):
    'Display details of a course with given title or ID'

    # select what arguments are accepted
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('title', help='Title of course to show')

        # add ID argument   !!!
        return parser

    # do something with the given args
    # ShowOne expects tuple with some (headers, values)
    def take_action(self, parsed_args):
        headers = data[0]
        for d in data[1:]:
            if d[0] == parsed_args.title:
                return (headers, d)
        return (None, None)


def main(argv=sys.argv[1:]):
    sync2folder = Sync2Folder()
    return sync2folder.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))