import numpy
from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_track(DataWrapper):
    def __init__(self, id, pose: numpy.ndarray=None, size: numpy.ndarray=None):
        super().__init__(id=id, dtypecate=DataTypeCategory.TRACK)
        self.pos = pose[:, 3]
        self.poseMatrix = pose
        self.size = size[:, 3]

        self.ref_point = 0
        self.acc = 0
        self.speed = 0

    def getPoint(self):
        return self.pos

    def getSize(self):
        return self.size