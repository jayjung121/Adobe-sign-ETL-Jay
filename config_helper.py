'''
This script help configuration of different matters including database, api and more.
'''
# Changed since ConfigParser has been renamed to configparser
import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def get(self, section):
        sectionDict = {}
        options = self.config.options(section)
        for option in options:
            try:
                sectionDict[option] = self.config.get(section, option)
                if sectionDict[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                sectionDict[option] = None
        return sectionDict