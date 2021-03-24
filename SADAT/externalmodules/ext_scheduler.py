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

    def doTask2(self):
        pass
        #DisAct_Track()

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

    # def get_dataset(self):
    #     return self._dataset.keys()
    #
    # def set_dataset(self,datakey,datatype):
    #     self._dataset[datakey]=datatype

    def addData(self, datakey, data, dictkey=None):
        dset = self._dataset[datakey]

        if isinstance(dset, list):
            dset.append(data)
        elif isinstance(dset, dict) and dictkey is not None:
            dset[dictkey] = data
        elif isinstance(dset, int):
            self._dataset[datakey] = data
        elif isinstance(dset, float):
            self._dataset[datakey] = data
        elif isinstance(dset, str):
            self._dataset[datakey] = data
        else:
            self._dataset[datakey] = None

    def copyAllData(self, datakey, data):
        """Copy All data
        This method is the reverse of `get_config`,
        capable of instantiating the same layer from the config
        dictionary. It does not handle layer connectivity
        (handled by Network), nor weights (handled by `set_weights`).
        Args:
            datakey: A Python dictionary, typically the
                key of data.
            data: actual data list, type will be various.
        """
        dset = self._dataset[datakey]
        if type(data) == type(dset):
            self._dataset[datakey] = data

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
        for rdata in data:
            self._rawdata[rdata[0]] = rdata[1]

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
