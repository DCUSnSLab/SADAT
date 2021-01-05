from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.tracker import trackerBasic
from externalmodules.extModule import extModule
from externalmodules.flow_wrapper import FlowWrapper


class senarioBasic(FlowWrapper):
    def __init__(self):
        super().__init__()
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