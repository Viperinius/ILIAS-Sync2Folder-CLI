import os
import sys

from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager

asciiLogo = r'''
 ___ _     ___    _    ____       ____                   ____  _____     _     _           
|_ _| |   |_ _|  / \  / ___|     / ___| _   _ _ __   ___|___ \|  ___|__ | | __| | ___ _ __ 
 | || |    | |  / _ \ \___ \ ____\___ \| | | | '_ \ / __| __) | |_ / _ \| |/ _` |/ _ \ '__|
 | || |___ | | / ___ \ ___) |_____|__) | |_| | | | | (__ / __/|  _| (_) | | (_| |  __/ |   
|___|_____|___/_/   \_\____/     |____/ \__, |_| |_|\___|_____|_|  \___/|_|\__,_|\___|_|   
                                        |___/                                              
===========================================================================================
'''

class Sync2Folder(App):
    def __init__(self):
        super().__init__(
            description='Download your ILIAS course files to your local disk automatically',
            version='0.1.0',
            command_manager=CommandManager('sync2folder.cli'),
            deferred_help=True,
        )
    
    # define what commands are available
    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        self.LOG.info(asciiLogo)

def main(argv=sys.argv[1:]):
    sync2folder = Sync2Folder()
    return sync2folder.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))