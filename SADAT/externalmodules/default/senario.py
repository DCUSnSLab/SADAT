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
        #set dataset to to be new data for viewing in planview
        self._dataset[senarioBasicDataset.TRACK] = list()
        self._dataset[senarioBasicDataset.CAMTRACK] = list()

        print('init senario basic')

    def dataConstruction(self):
        self._addDataset('tracker', dtype_tracker())
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