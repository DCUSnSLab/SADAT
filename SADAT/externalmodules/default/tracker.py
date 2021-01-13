from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule


class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')

    def do(self):
        tdata = dtype_tracker(0, 300, 10, 20, 50)
        self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)
        #print('do ExtModules -->', self.getName())