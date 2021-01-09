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

    def isEnabled(self):
        return self.__Enabled

    def getName(self):
        return self.__name

    #깊은복사?? 메모리 주소만 옮겨줄까.. 아님 모조리 카피??
    def _addData(self, datakey, data, dictkey=None):
        self._scheduler.addData(datakey, data, dictkey)

    def _getDataKeys(self):
        return self._scheduler.getDataKeys()

    def _getData(self, key):
        return self._scheduler.getData(key)

    def _getAllDataset(self):
        return self._scheduler.getAllRawDataset()

    def _getRawDataKeys(self):
        return self._scheduler.getRawDataKeys()

    def _getRawDatabyKey(self, key):
        return self._scheduler.getRawData(key)

    def _getAllRawData(self):
        return self._scheduler.getAllRawDataset()

    # def dataTransfer(self, idata:dict):
    #     for ikey, ivalue in idata.items():
    #         self.__rawdata[ikey] = ivalue
