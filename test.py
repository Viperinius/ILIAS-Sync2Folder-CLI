from iliasHandling import IliasHandling

handler = IliasHandling()

print("Login...")
user = input('user: ')
password = input('pw: ')

loggedin = handler.iliasLogin(user, password)

print(loggedin)

handler.getCourseIds()

handler.getCourseNames()

loggedout = handler.iliasLogout()

print(loggedout)