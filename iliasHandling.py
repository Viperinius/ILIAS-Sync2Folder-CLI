from config import Config
from zeep import Client
import untangle

class IliasHandling:
    wsdl = 'https://nbl.fh-bielefeld.de/webservice/soap/server.php?wsdl'

    loggedIn = False
    config = Config()
    client = Client(wsdl=wsdl)

    sessionId = ""
    userId = 0

    courseList = []

    def __init__(self):
        pass

    def iliasLogin(self, user, password):
        """
        Log in to ILIAS,
        Returns false if not successful
        """
        if self.loggedIn:
            return True
        else:
            if (user != '' and password != ''):
                self.config.setUser = user

                # connect to ILIAS SOAP
                try:
                    # get session id / log in
                    self.sessionId = self.client.service.loginLDAP(self.config.getClient(), user, password)
                    self.userId = self.client.service.getUserIdBySid(self.sessionId)
                    self.loggedIn = True
                    return True
                except:
                    print('Error while logging in!')
                    self.loggedIn = False
                    return False
            else:
                self.loggedIn = False
                return False

    def iliasLogout(self):
        """
        Log out of ILIAS,
        Returns true if successful
        """
        if self.loggedIn:
            self.loggedIn = False
            return self.client.service.logout(self.sessionId)
        else:
            return False

    def getCourseIds(self):
        """
        Get IDs of the courses the user is in, (re)fills the courseList
        """
        self.courseList.clear()

        if not self.loggedIn:
            return
        
        xmlUserRoles = untangle.parse(self.client.service.getUserRoles(self.sessionId, self.userId))

        # scan for "Title" tags (contain the roles with the course ids), add course ids to list
        for obj in xmlUserRoles.Objects.Object:
            role = obj.Title.cdata

            if (role.startswith('il_crs_member') or role.startswith('il_crs_tutor')):
                tmp = role.split('_')
                
                # filter "FSR" course of FH Bielefeld (temporary solution :/)
                if tmp[3] != '39643':
                    self.courseList.append(CourseInfo(courseId=tmp[3]))

    def getCourseNames(self):
        """
        Collect course names matching the course ids
        """
        for course in self.courseList:
            course.courseName = self.getCourseName(course.courseId)

    def getCourseName(self, ref):
        """
        Retrieve course name from given course id
        """
        xmlCourse = untangle.parse(self.client.service.getObjectByReference(self.sessionId, int(ref), self.userId))
        return xmlCourse.Objects.Object.Title.cdata







class CourseInfo:
    courseChecked = False
    courseName = ''
    courseOwnName = ''
    courseId = ''

    def __init__(self, courseChecked=False, courseName='', courseOwnName='', courseId=''):
        self.courseChecked = courseChecked
        self.courseName = courseName
        self.courseOwnName = courseOwnName
        self.courseId = courseId