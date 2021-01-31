from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule
import mytracker # Project Structure에서 Tracker Project를 추가하여야 함

from random import *

from sensor.SenAdptMgr import AttachedSensorName

class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')
        self.tracker = mytracker.Tracker(60, 2)
        # self.track_xy = mytracker.dbscanClustering(60, 2) # eps, min_samples

    def getRawDatabyKey(self, key):
        return self._getRawDatabyKey(key)

    def getLidarDatabyKey(self, key):
        return self._getData()

    def do(self):
        # tracker_x, tracker_y, height, width = mytracker.getlidardata(self)
        # tracker_list = mytracker.getlidardata(self)
        tracker_list = self.tracker.getlidardata(self)

        for idx, tracker_x, tracker_y in tracker_list:
            tdata = dtype_tracker(idx, tracker_x, tracker_y, 10, 10)
            self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)
        # TODO mytracker.getlidardata의 리턴값을 tracker_x, tracker_y, (x, y), (x, y) 로 수정하여야 함.
        # mytracker 코드에서 height, width 값을 가져오도록 되어있는데,
        # 제대로 된 Tracker 구현 이후 생성된 Tracker의 좌하단, 우상단 좌표값을 가져오는 코드로
        # 수정 진행하여야 함.
        # tdata = dtype_tracker(0, 10, 10, 50, 50)
        # self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)
        #print('do ExtModules -->', self.getName())