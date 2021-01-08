from abc import *

from dadatype.dtype_rplidar import dtype_rplidar
from externalmodules.extModule import extModule

'''
1. 외부 모듈 시나리오 모듈 래퍼
2. 이곳에서 정한 순서대로 외부모듈 동작됨
'''
class extScheduler(metaclass=ABCMeta):
    def __init__(self):
        self._modules = list()
        self._rawdata = dict()
        self._dataset = dict()

    def initextScheduler(self):
        self.dataConstruction()
        self.modConstruction()

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

    def _addDataset(self, name, datatype):
        self._dataset[name] = datatype

    def insertRawData(self, data):
        #Temporary.. exchange data type from raw data to dtype_rplidar
        key = 'rplidar'
        if key in self._rawdata:
            self._dataset[key].clear()
        else:
            self._dataset[key] = list()

        for idx in range(0, len(data[0]), 1):
            # print(idx)
            #print(data)
            posx = data[0]
            posy = data[1]
            tstmp = data[2]
            # print(posx[0])
            pdata = dtype_rplidar(idx, posx[idx], posy[idx])
            self._dataset[key].append(pdata)
        # posx = data[0]
        # posy = data[1]
        # tstmp = data[2]
        #print(data)

    @abstractmethod
    def dataConstruction(self):
        pass

    @abstractmethod
    def modConstruction(self):
        pass
