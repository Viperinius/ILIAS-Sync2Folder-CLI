#from iliasHandling import IliasHandling
#from helpers import Helpers
#from config import Config
#from getpass import getpass

# config = Config()
#handler = IliasHandling()
#helper = Helpers()

#helper.gatherCourseNames()

# #config.setPath('/home/alexander/test')
# config.setPath('X:\\Test')

# print("Login...")
# user = input('user: ')
# password = getpass('pw: ')

# loggedin = handler.iliasLogin(user, password)
#print(handler.sessionId)

#print('user id: ')
#print(handler.userId)

#print ('---')
#print(handler.client.service.getUserIdBySid(handler.sessionId))

#print(handler.recoverSession())

#print(handler.sessionId)

#handler.getCourseIds()

# #handler.getCourseNames()

# #handler.getCourseFiles(596778)

# #from iliasHandling import FileInfo
# #handler.getSingleFile(FileInfo('', 'test.pdf', 'X:\\Test', '', '', 602980, '', ''))

# #for file in handler.fileList:
# #    handler.createDirectories(file.filePath, 596778, False)

# #handler.testing(602980)


# loggedout = handler.iliasLogout()
# print(loggedout)


d = {
    479495: 'Blah', 
    596777: 'Energietechnik', 
    596778: 'HF und EMV'
}

if 479495 in d:
    print('hurray')
else:
    print('nope')