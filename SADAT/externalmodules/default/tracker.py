from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule
import mytracker # Project Structure에서 Tracker Project를 추가하여야 합니다.

from sensor.SenAdptMgr import AttachedSensorName

class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')
        self.tracker = mytracker.Tracker(100, 2)

    def getRawDatabyKey(self, key):
        return self._getRawDatabyKey(key)

    def getLidarDatabyKey(self, key):
        return self._getData()

    def do(self):
        tracker_list = self.tracker.getlidardata(self)

        for tracker_x, tracker_y, idx, minX, maxX, minY, maxY in tracker_list:
            tdata = dtype_tracker(idx, minX, maxX, minY, maxY, tracker_x, tracker_y, maxX - minX, maxY - minY)
            self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)