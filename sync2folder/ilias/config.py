import yaml
import os

configFilePath = os.path.dirname(__file__)

class Config:
    yamlConf = ""

    tempFile = '.s2fTmp'

    def __init__(self):
        self.reloadFile()

    def reloadFile(self):
        with open(os.path.join(configFilePath, 'config.yaml'), 'r', encoding='utf8') as conf:
            self.yamlConf = yaml.safe_load(conf)

    def updateFile(self):        
        with open(os.path.join(configFilePath, 'config.yaml'), 'w', encoding='utf8') as conf:
            yaml.dump(self.yamlConf, conf, default_flow_style=False)

    def readSessionId(self):
        if not os.path.isfile(os.path.join(configFilePath, self.tempFile)):
            return ''
        with open(os.path.join(configFilePath, self.tempFile), 'r') as temp:
            return str(temp.read())

    def writeSessionId(self, sessionId):
        with open(os.path.join(configFilePath, self.tempFile), 'w') as temp:
            pass
        with open(os.path.join(configFilePath, self.tempFile), 'w') as temp:
            temp.write(sessionId)

    def setFromServerUri(self):
        """
        Set WSDL and client ID from server link
        """
        self.reloadFile()
        uri = self.getServerUri()

        uri = ''
        if '/login.php' in uri:
            linkParts = uri.split('client_id=')
            if len(linkParts) > 1:
                if '&' in linkParts[1]:
                    clientId = linkParts[1].split('&')[0]
                else:
                    clientId = linkParts[1]
                self.setClient(clientId)
            #else:
                # implement fetching of client id   !!!
            
            wsdl = uri.replace('login.php', 'webservice/soap/server.php?wsdl')
            self.setWsdlUri(wsdl)

        # maybe accept webservice link too?
        

    ########################################################
    #               Connection settings
    ########################################################

    def getClient(self):
        self.reloadFile()
        return self.yamlConf['connection']['client']

    def setClient(self, client):
        self.yamlConf['connection']['client'] = client
        self.updateFile()

    def getServerUri(self):
        self.reloadFile()
        return self.yamlConf['connection']['serverURI']

    def setServerUri(self, server):
        self.yamlConf['connection']['serverURI']
        self.updateFile()

    def getUser(self):
        self.reloadFile()
        return self.yamlConf['connection']['user']

    def setUser(self, user):
        self.yamlConf['connection']['user'] = user
        self.updateFile()

    def getUserId(self):
        self.reloadFile()
        return self.yamlConf['connection']['userId']

    def setUserId(self, userId):
        self.yamlConf['connection']['userId'] = userId
        self.updateFile()

    def getWsdlUri(self):
        self.reloadFile()
        return self.yamlConf['connection']['wsdl']

    def setWsdlUri(self, wsdl):
        self.yamlConf['connection']['wsdl'] = wsdl
        self.updateFile()

    ########################################################
    #               Course settings
    ########################################################

    def getCourseInfo(self, course):
        self.reloadFile()
        if course in self.yamlConf['courses']:
            return self.yamlConf['courses'][course]
        else:
            return {}

    def setCourseInfo(self, course, name='-1', sync='-1'):
        if name == '-1' and sync == '-1':
            return
        else:
            if course not in self.yamlConf['courses']:
                self.yamlConf['courses'][course] = {}

            if name != '-1':
                self.setCourseName(course, name)
            if sync != '-1':
                self.setCourseSync(course, sync)
            self.updateFile()

    def clearCourses(self):
        self.yamlConf['courses'] = {}
        self.updateFile()

    def getCourseSync(self, course):
        self.reloadFile()
        if course in self.yamlConf['courses']:
            return self.yamlConf['courses'][course]['sync']
        else:
            return False

    def setCourseSync(self, course, boolean):
        if course in self.yamlConf['courses']:
            self.yamlConf['courses'][course]['sync'] = boolean
            self.updateFile()

    def getCourseName(self, course):
        self.reloadFile()
        if course in self.yamlConf['courses']:
            if 'name' in self.yamlConf['courses'][course]:
                return self.yamlConf['courses'][course]['name']
            return ''
        else:
            return ''

    def setCourseName(self, course, name):
        if course in self.yamlConf['courses']:
            self.yamlConf['courses'][course]['name'] = name
            self.updateFile()


    ########################################################
    #               LocalDir settings
    ########################################################

    def getPath(self):
        self.reloadFile()
        return self.yamlConf['localDir']['path']

    def setPath(self, path):
        self.yamlConf['localDir']['path'] = path
        self.updateFile()

    def getStructTemplate(self):
        self.reloadFile()
        return self.yamlConf['localDir']['structureTemplate']

    def setStructTemplate(self, template):
        self.yamlConf['localDir']['structureTemplate'] = template
        self.updateFile()

    def getUseOwnNames(self):
        self.reloadFile()
        return self.yamlConf['localDir']['useOwnNames']
    
    def setUseOwnNames(self, boolean):
        self.yamlConf['localDir']['useOwnNames'] = boolean
        self.updateFile()

    def getUseOwnStructure(self):
        self.reloadFile()
        return self.yamlConf['localDir']['useOwnStructure']

    def setUseOwnStructure(self, boolean):
        self.yamlConf['localDir']['useOwnStructure'] = boolean
        self.updateFile()

    def getUseYearInStructure(self):
        self.reloadFile()
        return self.yamlConf['localDir']['useYear']

    def setUseYearInStructure(self, boolean):
        self.yamlConf['localDir']['useYear'] = boolean
        self.updateFile()

    ########################################################
    #               Sync settings
    ########################################################

    def getOverwriteAll(self):
        self.reloadFile()
        return self.yamlConf['sync']['overwrite']

    def setOverwriteAll(self, boolean):
        self.yamlConf['sync']['overwrite'] = boolean
        self.updateFile()

    def getOverwriteNone(self):
        self.reloadFile()
        return self.yamlConf['sync']['owIgnore']

    def setOverwriteNone(self, boolean):
        self.yamlConf['sync']['owIgnore'] = boolean
        self.updateFile()

    def getFileIgnore(self, fileId):
        self.reloadFile()
        if fileId in self.yamlConf['sync']['ignoredFiles']:
            return self.yamlConf['sync']['ignoredFiles'][fileId]
        else:
            return False

    def setFileIgnore(self, fileId, boolean):
        self.yamlConf['sync']['ignoredFiles'][fileId] = boolean
        self.updateFile()

    def getShowNew(self):
        self.reloadFile()
        return self.yamlConf['sync']['showNew']

    def setShowNew(self, boolean):
        self.yamlConf['sync']['showNew'] = boolean
        self.updateFile()

    def getShowOnly(self):
        self.reloadFile()
        return self.yamlConf['sync']['showOnly']

    def setShowOnly(self, boolean):
        self.yamlConf['sync']['showOnly'] = boolean
        self.updateFile()

    def getSyncAll(self):
        self.reloadFile()
        return self.yamlConf['sync']['syncAll']

    def setSyncAll(self, boolean):
        self.yamlConf['sync']['syncAll'] = boolean
        self.updateFile()

    def getSyncNotify(self):
        self.reloadFile()
        return self.yamlConf['sync']['syncNotification']

    def setSyncNotify(self, boolean):
        self.yamlConf['sync']['syncNotification'] = boolean
        self.updateFile()

    ########################################################
    #               System settings
    ########################################################

    def getLang(self):
        self.reloadFile()
        return self.yamlConf['system']['lang']

    def setLang(self, lang):
        self.yamlConf['system']['lang'] = lang
        self.updateFile()
    
    def getTheme(self):
        self.reloadFile()
        return self.yamlConf['system']['theme']

    def setTheme(self, theme):
        self.yamlConf['system']['theme'] = theme
        self.updateFile()

    def getTrayIcon(self):
        self.reloadFile()
        return self.yamlConf['system']['trayicon']

    def setTrayIcon(self, boolean):
        self.yamlConf['system']['trayicon']
        self.updateFile()

    def getUpdateCheck(self):
        self.reloadFile()
        return self.yamlConf['system']['updateCheck']

    def setUpdateCheck(self, boolean):
        self.yamlConf['system']['updateCheck'] = boolean
        self.updateFile()