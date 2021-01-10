from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule
import copy

class delayedPoints(extModule):
    def __init__(self):
        super().__init__('delayedPoints')
        self.prevdata = None

    def do(self):
        key = self._scheduler.tempRawKey
        datas = self._getRawDatabyKey(key)

        if self.prevdata is None:
            self.prevdata = datas
            # self.prevdata = list()
            # for data in datas:
            #     self.prevdata.append(data)

        else:
            #self._copyAllData(datakey=senarioBasicDataset.DELAYEDPOINTS, data=self.prevdata)
            for data in self.prevdata:
                #얇은 복사로 넣어줘야 하나?
                self._addData(datakey=senarioBasicDataset.DELAYEDPOINTS, data=data)

            #self.prevdata.clear()
            self.prevdata = copy.deepcopy(datas)
            # for data in datas:
            #     self.prevdata.append(data)
