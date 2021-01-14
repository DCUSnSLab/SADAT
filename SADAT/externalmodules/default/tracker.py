from dadatype.dtype_tracker import dtype_tracker
from externalmodules.default.dataset_enum import senarioBasicDataset
from externalmodules.extModule import extModule
import mytracker # Project Structure에서 Tracker Project를 추가하여야 함

from random import *

from sensor.SenAdptMgr import AttachedSensorName

class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')
        # self.track_xy = mytracker.dbscanClustering(60, 2) # eps, min_samples

    def getRawDatabyKey(self, key):
        return self._getRawDatabyKey(key)

    def getLidarDatabyKey(self, key):
        return self._getData()

    def do(self):
        # tdata = dtype_tracker(0, 300, 10, 20, 50)

        tracker_x, tracker_y = mytracker.getlidardata(self)
        # tdata = dtype_tracker(0, 10, 10, 50, 50)
        # tdata = dtype_tracker(0, randrange(200), randrange(200), 50, 50)
        tdata = dtype_tracker(0, tracker_x, tracker_y, 50, 50)
        self._addData(datakey=senarioBasicDataset.TRACK, data=tdata)
        #print('do ExtModules -->', self.getName())