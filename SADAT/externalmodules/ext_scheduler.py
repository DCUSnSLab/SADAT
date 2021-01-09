from abc import *

from dadatype.dtype_rplidar import dtype_rplidar
from externalmodules.extModule import extModule

'''
1. 외부 모듈 시나리오 모듈 래퍼
2. 이곳에서 정한 순서대로 외부모듈 동작됨
'''
class extScheduler(metaclass=ABCMeta):
    def __init__(self):
        self.tempRawKey = 'rplidar'
        self._modules = list()
        self._rawdata = dict()
        self._dataset = dict()

    def initextScheduler(self):
        self.dataConstruction()
        self.modConstruction()

    def doTask(self):
        for mod in self._modules:
            if mod.isEnabled():
                mod.do()

    def _addModules(self, modlist):
        for mod in modlist:
            mod.addScheduler(self)
            self._addModule(mod)

    def _addModule(self, mod:extModule):
        self._modules.append(mod)

    def getModules(self):
        return self._modules

    def disableModule(self, idx):
        mod = self._modules[idx]
        mod.setEnable(False)

    def enableModule(self, idx):
        mod = self._modules[idx]
        mod.setEnable(True)

    def _initDataset(self, datakey, datatype):
        self._dataset[datakey] = datatype

    def addData(self, datakey, data, dictkey=None):
        dset = self._dataset[datakey]

        if isinstance(dset, list):
            dset.append(data)
        elif isinstance(dset, dict) and dictkey is not None:
            dset[dictkey] = data
        elif isinstance(dset, int):
            dset = data
        elif isinstance(dset, float):
            dset = data
        elif isinstance(dset, str):
            dset = data
        else:
            dset = None

    def getDataKeys(self):
        return self._dataset.keys()

    def getData(self, key):
        if key in self._dataset:
            return self._dataset[key]
        else:
            return None

    def getAllDataset(self):
        return self._dataset

    def insertRawData(self, data):
        #Temporary.. exchange data type from raw data to dtype_rplidar
        key = self.tempRawKey
        if key in self._rawdata:
            self._rawdata[key].clear()
        else:
            self._rawdata[key] = list()

        for idx in range(0, len(data[0]), 1):
            # print(idx)
            #print(data)
            posx = data[0]
            posy = data[1]
            tstmp = data[2]
            pdata = dtype_rplidar(idx, posx[idx], posy[idx])
            self._rawdata[key].append(pdata)

    def getRawDataKeys(self):
        return self._rawdata.keys()

    def getRawData(self, key):
        if key in self._rawdata:
            return self._rawdata[key]
        else:
            return None

    def getAllRawDataset(self):
        return self._rawdata

    def resetData(self):
        self.__resetData(self._rawdata)
        self.__resetData(self._dataset)

    def __resetData(self, idata):
        for dgroup in idata.values():
            if isinstance(dgroup, dict) or isinstance(dgroup, list):
                dgroup.clear()
            else:
                dgroup = 0


    @abstractmethod
    def dataConstruction(self):
        pass

    @abstractmethod
    def modConstruction(self):
        pass
