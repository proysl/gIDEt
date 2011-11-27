import ConfigParser

class ReadProperties:

    SECTION = "Basic"
    PROJECT_TYPE = "projectType"
    PROJECT_NAME = "projectName"

    def __init__(self):
        self.configParser = ConfigParser.RawConfigParser()

    def read(self, path):
        self.configParser.read(path)

    def sections(self):
        return self.configParser.sections()

    def options(self, section):
        self.configParser.options(section)

    def get(self, section, key):
        self.configParser.options(section, key)

    def getProjectType(self):
        return self.configParser.get(self.SECTION, self.PROJECT_NAME)

    def getProjectName(self):
        return self.configParser.get(self.SECTION, self.PROJECT_NAME)
