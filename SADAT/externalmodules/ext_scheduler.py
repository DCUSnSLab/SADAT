from abc import *
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
        posx = data[0]
        posy = data[1]
        tstmp = data[2]
        print(data)

    @abstractmethod
    def dataConstruction(self):
        pass

    @abstractmethod
    def modConstruction(self):
        pass
