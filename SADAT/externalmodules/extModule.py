from abc import *

'''
외부 모듈 래
'''
class extModule():
    def __init__(self, name, scheduler=None):
        self._scheduler = scheduler
        self.__name = name
        self.__Enabled = True
        #self.__rawdata = dict()

    def do(self):
        pass

    def addScheduler(self, scheduler):
        self._scheduler = scheduler

    def setEnable(self, bool):
        self.__Enabled = bool

    def getName(self):
        return self.__name

    # def dataTransfer(self, idata:dict):
    #     for ikey, ivalue in idata.items():
    #         self.__rawdata[ikey] = ivalue
