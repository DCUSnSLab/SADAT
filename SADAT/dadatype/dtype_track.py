import numpy
from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_track(DataWrapper):
    def __init__(self, id, isPoseData, pose: numpy.ndarray=None, size: numpy.ndarray=None
                 ,posf: numpy.ndarray=None, sizef: numpy.ndarray=None):
        super().__init__(id=id, dtypecate=DataTypeCategory.TRACK)

        if isPoseData:
            self.pos = pose[:, 3]
            self.poseMatrix = pose
            self.size = size[:, 3]
        else:
            self.pos = posf
            self.size = sizef
        self.ref_point = 0
        self.acc = 0
        self.speed = 0
        self.TID = 0

    def getPoint(self):
        return self.pos

    def getSize(self):
        return self.size

    def setPose(self, pos):
        self.pos = pos

    def setSize(self, size):
        self.size = size

    def setTID(self, tid):
        self.TID = tid