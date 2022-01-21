import numpy

from dadatype.dtype_cate import DataTypeCategory
from dadatype.dtype_track import dtype_track
from dadatype.grp_objects import grp_objects
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
from utils.importer import Importer


class ZedTrack(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Track, name)

    def _doWorkDataInput(self, objs):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        header = objs.header
        tracks = grp_objects(dtypecate=DataTypeCategory.TRACK, timestamp=header.stamp)
        for i in range(20):
            tracks.addObject(dtype_track(i, False, posf=numpy.array([0, 0, 0])
                                         , sizef=numpy.array([1, 1, 1])))
        tid = 0  # temporary id
        for obj in objs.objects:
            label = obj.label
            lid = obj.label_id
            # print(label, lid, ':', obj.position[0], obj.position[1], obj.position[2], obj.tracking_state
            #       , obj.confidence, obj.action_state)

            #track = dtype_track(tid, False, posf=obj.position, sizef=numpy.array([1, 1, 1]))
            track = tracks.getObjects()[tid]
            track.setPose(obj.position)
            track.setTID(obj.label_id)
            #print(track.pos)
            #tracks.addObject(track)
            tid += 1
        self.addRealtimeData(tracks)
        # print('-------------------')
        # poses = inputdata.poses
        #
        # #현재 pose array에서 2개의 pose가 1개의 트랙정보로 들어오는 중
        # #pose 0 : 트랙 pos and orientation
        # #pose 1 : 트랙 size
        # tdatas = list()
        # tracks = grp_objects(dtypecate=DataTypeCategory.TRACK, timestamp=header.stamp)
        # tid = 0 #temporary id
        # for i, ps in enumerate(poses):
        #     pdata = ros_numpy.numpify(ps)
        #     tdatas.append(pdata)
        #     if (i+1) % 2 == 0:
        #         track = dtype_track(tid, tdatas[0], tdatas[1])
        #         tracks.addObject(track)
        #         tdatas.clear()
        #         tid += 1
        # self.addRealtimeData(tracks)