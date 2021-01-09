from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule


class delayedPoints(extModule):
    def __init__(self):
        super().__init__('delayedPoints')
        self.prevdata = None

    def do(self):
        key = self._scheduler.tempRawKey
        datas = self._getRawDatabyKey(key)

        if  self.prevdata is None:
            self.prevdata = list()
            for data in datas:
                self.prevdata.append(data)

        else:
            for data in self.prevdata:
                #얇은 복사로 넣어줘야 하나?
                self._addData(datakey=senarioBasicDataset.DELAYEDPOINTS, data=data)

            self.prevdata.clear()
            for data in datas:
                self.prevdata.append(data)
