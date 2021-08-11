from dadatype.dtype_cate import DataTypeCategory
from dadatype.dtype_track import dtype_track
from dadatype.grp_objects import grp_objects
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
from utils.importer import Importer


class Track(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Track, name)

    def _doWorkDataInput(self, inputdata):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        header = inputdata.header
        poses = inputdata.poses

        #현재 pose array에서 2개의 pose가 1개의 트랙정보로 들어오는 중
        #pose 0 : 트랙 pos and orientation
        #pose 1 : 트랙 size

        tdatas = list()
        tracks = grp_objects(dtypecate=DataTypeCategory.TRACK, timestamp=header.stamp)
        tid = 0 #temporary id
        for i, ps in enumerate(poses):
            pdata = ros_numpy.numpify(ps)
            tdatas.append(pdata)
            if (i+1) % 2 == 0:
                track = dtype_track(tid, tdatas[0], tdatas[1])
                tracks.addObject(track)
                tdatas.clear()
                tid += 1
        self.addRealtimeData(tracks)