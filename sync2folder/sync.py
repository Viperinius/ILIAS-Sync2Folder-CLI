from cliff.command import Command
from cliff.lister import Lister

from sync2folder.ilias.iliasHandling import IliasHandling
import subprocess

handler = IliasHandling()

# ANSI code templates
colReset = '\33[0m'
bold = '\33[1m'
fgGreen = '\33[32m'
fgRed = '\33[31m'
fgCyan = '\033[36m'

tableHeader = '''
+---------------+-----------------------------------+-------------------------------------------+------------+-----------+-----------------+
| Status        | File Name                         | Path                                      | Date       | Size      | Updates ignored |
+---------------+-----------------------------------+-------------------------------------------+------------+-----------+-----------------+
'''
tableHeaderMinimal = '''
+---------------+-----------------------------------+
| Status        | File Name                         |
+---------------+-----------------------------------+
'''
tableFooter = '''
+---------------+-----------------------------------+-------------------------------------------+------------+-----------+-----------------+
'''
tableFooterMinimal = '''
+---------------+-----------------------------------+
'''

def constructRow(minimal, values, statusCol=colReset):
    'Generate table row from given data'
    # widths
    statusMax = 15
    nameMax = 35
    pathMax = 43
    dateMax = 12
    sizeMax = 11
    ignoredMax = 17


    status = (values[0][:(statusMax - 4)] + '.. ') if len(values[0]) > (statusMax - 4) else values[0]
    name = (values[1][:(nameMax - 4)] + '.. ') if len(values[1]) > (nameMax - 4) else values[1]

    row = '|'
    row += statusCol + (' ' + status).ljust(statusMax) + colReset + '|'
    row += (' ' + name).ljust(35) + '|'

    if not minimal:
        path = (values[2][:(pathMax - 4)] + '.. ') if len(values[2]) > (pathMax - 4) else values[2]
        date = (values[3][:(dateMax - 4)] + '.. ') if len(values[3]) > (dateMax - 4) else values[3]
        size = (values[4][:(sizeMax - 4)] + '.. ') if len(values[4]) > (sizeMax - 4) else values[4]
        ignored = (values[5][:(ignoredMax - 4)] + '.. ') if len(values[5]) > (ignoredMax - 4) else values[5]

        row += (' ' + path).ljust(pathMax) + '|'
        row += (' ' + date).ljust(dateMax) + '|'
        row += (' ' + size).ljust(sizeMax) + '|'
        row += (' ' + ignored).ljust(ignoredMax) + '|'

    row += '\n'
    return row

def startSync(optionalArgs, stdout):
    # https://stackoverflow.com/questions/12492810/python-how-can-i-make-the-ansi-escape-codes-to-work-also-in-windows/51524239#51524239
    subprocess.call('', shell=True)
    
    # show table header
    if optionalArgs.minimal:
        stdout.write(colReset + bold + tableHeaderMinimal + colReset)
    else:
        stdout.write(colReset + bold + tableHeader + colReset)

    import time

    stdout.write(constructRow(False, ['Missing', 'b', 'X:', '11.11.11', '1 KB', 'No']))
    stdout.write(constructRow(False, ['Missinggggggg', 'a', 'C:', '99.99.99', '1000 TB', 'Yes']))
    stdout.write(constructRow(False, ['Missing', 'd', 'A:', '32.3.2', '1 MB', 'Yes']))

    time.sleep(1)

    stdout.write('\033[3F' + constructRow(False, ['New', 'b', 'X:', '11.11.11', '1 KB', 'No'], fgGreen))
    time.sleep(1)
    stdout.write(constructRow(False, ['Error', 'a', 'C:', '99.99.99', '1000 TB', 'Yes'], fgRed))
    time.sleep(1)
    stdout.write(constructRow(False, ['Update available', 'd', 'A:', '32.3.2', '1 MB', 'Yes'], fgCyan))
    #stdout.write('\033[B')


    stdout.write('\033[F')
    if optionalArgs.minimal:
        stdout.write(colReset + bold + tableFooterMinimal + colReset)
    else:
        stdout.write(colReset + bold + tableFooter + colReset)
    stdout.write(colReset)

def stopSync():
    pass


