from config import Config

class Helpers:
    config = Config()

    def __init__(self):
        pass


    def getSemesterNum(self, courseName):
        """
        Get the semester number from a course name
        """
        # example: ELM-4.3-Embe...
        parts = courseName.split('-')
        # 4.3
        try:
            parts2 = parts[1].split('.')
            # 4
            return int(parts2[0])
        except:
            return 0

    def getCourseYear(self, courseName):
        """
        Get the semester year of the course
        """
        # example: ..., Wetter, SS2018
        parts = courseName.split(',')
        # SS2018 (or WS2017-18)
        try:
            if 'SS' in parts[len(parts) - 1]:
                parts2 = parts[len(parts) - 1].split('S')
                # 2018
                return parts2[2]
            else:
                parts2 = parts[len(parts) - 1].split('S')
                return parts2[1]
        except:
            return ''

    def replaceTemplatePlaceholder(self, courseName, structTemplate=""):
        """
        Replace the folder template with semester num and year
        """
        semesterNum = self.getSemesterNum(courseName)

        if semesterNum == 0:
            return "Allgemein"

        courseYear = self.getCourseYear(courseName)

        tmp = structTemplate.replace('%', str(semesterNum))
        if self.config.getUseYearInStructure():
            if courseYear == '':
                return tmp.replace('$', '')
            else:
                return tmp.replace('$', courseYear)
        else:
            return tmp.replace('$', '')


    def getPercentage(self, current, maximum):
        """
        Calculate percentage of given values
        """
        return '%.0f'%((current / maximum) * 100)

    def getSizeInKiB(self, sizeInByte):
        """
        Convert Byte to Kibibyte
        """
        return '%.1f'%(sizeInByte / 1024)

    def getSizeInMiB(self, sizeInByte):
        """
        Convert Byte to Mebibyte
        """
        return '%.1f'%((sizeInByte / 1024) / 1024)