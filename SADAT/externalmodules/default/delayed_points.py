from dadatype.grp_rplidar import grp_rplidar
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule
import copy

from sensor.SenAdptMgr import AttachedSensorName


class delayedPoints(extModule):
    def __init__(self):
        super().__init__('delayedPoints')
        self.prevdata = None

    def do(self):
        key = AttachedSensorName.RPLidar2DVirtual
        dataObj = self._getRawDatabyKey(key)

        if self.prevdata is None:
            self.prevdata = grp_rplidar()
            self.prevdata.clone(dataObj)
            # self.prevdata = list()
            # for data in datas:
            #     self.prevdata.append(data)

        else:
            #self._copyAllData(datakey=senarioBasicDataset.DELAYEDPOINTS, data=self.prevdata)
            #얇은 복사로 넣어줘야 하나?
            self._addData(datakey=senarioBasicDataset.DELAYEDPOINTS, data=self.prevdata)

            #self.prevdata.clear()
            self.prevdata = grp_rplidar()
            self.prevdata.clone(dataObj)
            # for data in datas:
            #     self.prevdata.append(data)
