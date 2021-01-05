from abc import *

'''
외부 모듈 래
'''
class extModule():
    def __init__(self, name):
        self.__name = name
        self.__Enabled = True
        self.__rawdata = dict()

    def do(self):
        pass

    def setEnable(self, bool):
        self.__Enabled = bool

    def getName(self):
        return self.__name

    def dataTransfer(self, idata:dict):
        for ikey, ivalue in idata.items():
            self.__rawdata[ikey] = ivalue
