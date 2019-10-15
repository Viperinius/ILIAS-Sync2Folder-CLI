from iliasHandling import IliasHandling
from config import Config
from getpass import getpass

config = Config()
handler = IliasHandling()

#config.setPath('/home/alexander/test')
config.setPath('X:\\Test')

print("Login...")
user = input('user: ')
password = getpass('pw: ')

loggedin = handler.iliasLogin(user, password)
print(loggedin)

#handler.getCourseIds()

#handler.getCourseNames()

#handler.getCourseFiles(596778)

#from iliasHandling import FileInfo
#handler.getSingleFile(FileInfo('', 'test.pdf', 'X:\\Test', '', '', 602980, '', ''))

#for file in handler.fileList:
#    handler.createDirectories(file.filePath, 596778, False)

#handler.testing(602980)


loggedout = handler.iliasLogout()
print(loggedout)
