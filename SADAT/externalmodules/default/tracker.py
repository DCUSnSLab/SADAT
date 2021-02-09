from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule


class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')

    def do(self):
        tdata = dtype_tracker(0, 0, 0, 10, 10)
        self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)
        tdata2 = dtype_tracker(1, 10, 0, 10, 10)
        self._addData(datakey=senarioBasicDataset.TRACK, data=tdata2)
        #print('do ExtModules -->', self.getName())