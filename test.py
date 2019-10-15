from iliasHandling import IliasHandling
from config import Config
from getpass import getpass

config = Config()
handler = IliasHandling()

config.setPath('/home/alexander/test')
#config.setPath('X:\\Test')

print("Login...")
user = input('user: ')
password = getpass('pw: ')

loggedin = handler.iliasLogin(user, password)
print(loggedin)

#handler.getCourseIds()

#handler.getCourseNames()

#handler.getCourseFiles(596778)

handler.getFileGzip(602980, '/home/alexander/test', 'ELM-7-EET_Leseanleitung.pdf', 'mup')

#for file in handler.fileList:
#    handler.createDirectories(file.filePath, 596778, False)




#loggedout = handler.iliasLogout()
#print(loggedout)
