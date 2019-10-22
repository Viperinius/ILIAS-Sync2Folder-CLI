from cliff.command import Command
from cliff.lister import Lister

from sync2folder.ilias.iliasHandling import IliasHandling
from getpass import getpass
import sync2folder.sync

import logging

handler = IliasHandling()

# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def strToBool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        # temp solution, maybe replace with sth different   !!!
        return False

class ShowConnection(Lister):
    'Displays connection info (server link, client ID etc.)'

    table = [
        ['Option', 'Current Value'],
        ['Login status', '' ],
        ['Server link', ''],
        ['Client ID', ''],
        ['Saved user name', ''],
        ['Saved user ID', ''],
        ['Saved session ID', ''],
    ]

    def take_action(self, parsed_args):
        if handler.loggedIn:
            self.table[1][1] = '√'
        else:
            self.table[1][1] = 'x'

        self.table[2][1] = handler.config.getServerUri()
        self.table[3][1] = handler.config.getClient()
        self.table[4][1] = handler.config.getUser()
        self.table[5][1] = handler.config.getUserId()
        self.table[6][1] = handler.config.readSessionId()

        return self.table[0], self.table[1:]

class SetConnection(Command):
    'Sets connection settings (one at a time)'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument('-s', '--server', nargs='?', help='Set the server URL')
        group.add_argument('-c', '--client', nargs='?', help='Set the client ID')
        group.add_argument('-n', '--name', nargs='?', help='Set the default user name')
        return parser

    def take_action(self, parsed_args):
        if parsed_args.server:
            handler.config.setServerUri(parsed_args.server)
        elif parsed_args.client:
            handler.config.setClient(parsed_args.client)
        elif parsed_args.name:
            handler.config.setUser(parsed_args.name)
        else:
            self.app.stdout.write('No setting given. Exited.\n')
            return
        self.app.stdout.write('Connection settings updated.\n')

class ShowDirectorySettings(Lister):
    'Displays directory settings'

    table = [
        ['Option', 'Current Value'],
        ['Root save path', ''],
        ['Use own folder structure', ''],
        ['Include year in structure', ''],
        ['Structure template', ''],
    ]

    def take_action(self, parsed_args):
        self.table[1][1] = handler.config.getPath()
        if handler.config.getUseOwnStructure():
            self.table[2][1] = '√'
        else:
            self.table[2][1] = 'x'

        if handler.config.getUseYearInStructure():
            self.table[3][1] = '√'
        else:
            self.table[3][1] = 'x'
        
        self.table[4][1] = handler.config.getStructTemplate()

        return self.table[0], self.table[1:]

class SetDirectorySettings(Command):
    'Sets directory settings (one at a time)'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument('-p', '--path', nargs='?', help='Set the root save path')
        group.add_argument('-s', '--structure', nargs='?', help='Set if you want to use your own folder structure', type=strToBool)
        group.add_argument('-y', '--year', nargs='?', help='Set if the year should be included in the structure', type=strToBool)
        group.add_argument('-t', '--template', nargs='?', help='Set the folder structure template')
        return parser
    
    def take_action(self, parsed_args):
        if parsed_args.path:
            handler.config.setPath(parsed_args.path)
        elif parsed_args.structure is not None:
            handler.config.setUseOwnStructure(parsed_args.structure)
        elif parsed_args.year is not None:
            handler.config.setUseYearInStructure(parsed_args.year)
        elif parsed_args.template:
            handler.config.setStructTemplate(parsed_args.template)
        else:
            self.app.stdout.write('No setting given. Exited.\n')
            return
        self.app.stdout.write('Directory settings updated.\n')

class ListCourses(Lister):
    "Displays the users' courses"

    table = [
        ['Course ID', 'Course Name', 'Own Name', 'Included in Sync'],
    ]

    def take_action(self, parsed_args):
        self.table.extend(sync2folder.sync.generateCourseList())

        return self.table[0], self.table[1:]

class EditCourses(Command):
    'Changes course settings'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument('-i', '--id', nargs='?', help='Course ID to use', type=int)
        group = parser.add_mutually_exclusive_group()

        group.add_argument('-s', '--select', action='store_true', help='Select a course with ID')
        group.add_argument('-d', '--deselect', action='store_true', help='Deselect a course with ID')
        group.add_argument('-a', '--selectall', action='store_true', help='Select all courses')
        group.add_argument('-n', '--selectnone', action='store_true', help='Deselect all courses')
        group.add_argument('-o', '--ownnames', nargs='?', help='Use / Do not use own names', type=strToBool)
        group.add_argument('-e', '--editname', nargs='?', help='Edit own course name')
        return parser

    def take_action(self, parsed_args):
        print(parsed_args)
        if parsed_args.id is None and (parsed_args.deselect or parsed_args.editname is not None or parsed_args.select):
            self.app.stdout.write('No course given (use -i or --id to provide one). Exited.\n')
            return

        if parsed_args.deselect and parsed_args.id is not None:
            handler.config.setCourseSync(parsed_args.id, False)
        elif parsed_args.editname is not None and parsed_args.id is not None:
            handler.config.setCourseName(parsed_args.id, parsed_args.editname)
        elif parsed_args.ownnames is not None:
            handler.config.setUseOwnNames(parsed_args.ownnames)
        elif parsed_args.select and parsed_args.id is not None:
            handler.config.setCourseSync(parsed_args.id, True)
        elif parsed_args.selectall:
            handler.config.setSyncAll(True)
        elif parsed_args.selectnone:
            handler.config.setSyncAll(False)
        else:
            self.app.stdout.write('No setting given. Exited.\n')
            return
        self.app.stdout.write('Course settings updated.\n')

class Sync(Command):
    'Start / Stop synchronising with or without options'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument('command', help='Use "start" or "stop" to choose what to do')

        groupFiles = parser.add_mutually_exclusive_group()
        groupFiles.add_argument('-o', '--overwrite', action='store_true', help='Overwrite all updated files')
        groupFiles.add_argument('-i', '--ignore', action='store_true', help='Ignore all updated files')

        parser.add_argument('-s', '--show', action='store_true', help='Show files ony without downloading them')
        parser.add_argument('-n', '--new', action='store_true', help='Show only new files')
        parser.add_argument('-m', '--minimal', action='store_true', help='Hide most file info except name and status')
        return parser

    def take_action(self, parsed_args):
        print(parsed_args)

        handler.config.setOverwriteNone(parsed_args.ignore)
        handler.config.setShowNew(parsed_args.new)
        handler.config.setOverwriteAll(parsed_args.overwrite)
        handler.config.setShowOnly(parsed_args.show)

        if parsed_args.command == 'start':
            sync2folder.sync.startSync(parsed_args, self.app.stdout)
        elif parsed_args.command == 'stop':
            sync2folder.sync.stopSync()
        
        return


class Login(Command):
    'Login to ILIAS'

    #log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('-u', '--user', nargs='?', help='Pass a user name instead of interactively asking')
        parser.add_argument('-p', '--password', nargs='?', help='Pass a password instead of interactively asking')
        parser.add_argument('-d', '--default', nargs='?', const='1', help='Use default / saved user name (is ignored if -u used too)')
        return parser

    def take_action(self, parsed_args):
        if parsed_args.user is not None:
            if parsed_args.password is not None:
                result = handler.iliasLogin(parsed_args.user, parsed_args.password)
                if result:
                    self.app.stdout.write('Login successful.\n')
                    return
                self.app.stdout.write('Login failed.\n')
                return
            password = getpass('Enter password: ')
            result = handler.iliasLogin(parsed_args.user, password)
            if result:
                self.app.stdout.write('Login successful.\n')
                return
            self.app.stdout.write('Login failed.\n')
            return
        
        if parsed_args.password is not None:
            if parsed_args.default is not None:
                user = handler.config.getUser()
            else:
                user = input('Enter user name: ')
            result = handler.iliasLogin(user, parsed_args.password)
            if result:
                self.app.stdout.write('Login successful.\n')
                return
            self.app.stdout.write('Login failed.\n')
            return

        if parsed_args.default is not None:
            user = handler.config.getUser()
        else:
            user = input('Enter user name: ')
        password = getpass('Enter password: ')
        result = handler.iliasLogin(user, password)
        if result:
            self.app.stdout.write('Login successful.\n')
            return
        self.app.stdout.write('Login failed.\n')
        return

class Logout(Command):
    'Logout from ILIAS'

    #log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        if not handler.trySessionRecover():
            return

        if handler.loggedIn:
            result = handler.iliasLogout()
            if result:
                self.app.stdout.write('Successfully logged out.\n')
                return
            self.app.stdout.write('Logout failed.\n')
            return
        self.app.stdout.write('Already logged out.\n')
        return