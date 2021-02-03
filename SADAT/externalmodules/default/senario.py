from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.default.delayed_points import delayedPoints
from externalmodules.default.tracker import trackerBasic
from externalmodules.extModule import extModule
from externalmodules.ext_scheduler import extScheduler
from enum import Enum

class senarioBasic(extScheduler):
    def __init__(self):
        super().__init__()
        print('init senario basic')

    def dataConstruction(self):
        self._initDataset(senarioBasicDataset.TRACK, list())
        self._initDataset(senarioBasicDataset.CAMTRACK, list()) #temporary

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