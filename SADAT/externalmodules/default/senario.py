from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.tracker import trackerBasic
from externalmodules.extModule import extModule
from externalmodules.ext_scheduler import extScheduler
from enum import Enum

class senarioBasicDataset(Enum):
    TRACK = 1
    CAMTRACK = 2

class senarioBasic(extScheduler):
    def __init__(self):
        super().__init__()
        print('init senario basic')

    def dataConstruction(self):
        self._addDataset(senarioBasicDataset.TRACK, list())
        self._addDataset(senarioBasicDataset.CAMTRACK, list()) #temporary
        self.sprint('data Construction loaded')
        for key in self._dataset.keys():
            self.sprint(key)

    def modConstruction(self):
        self._addModules([trackerBasic()])
        self.sprint('load Modules')
        for mod in self._modules:
            self.sprint(mod.getName())


    def sprint(self, val):
        print('senarioBasic ====> ',val)