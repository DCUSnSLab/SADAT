import numpy
from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_track(DataWrapper):
    def __init__(self, id, isPoseData, pose: numpy.ndarray=numpy.array([0., 0., 0.]), size: numpy.ndarray=numpy.array([0., 0., 0.])
                 ,posf: numpy.ndarray=numpy.array([0., 0., 0.]), sizef: numpy.ndarray=numpy.array([0., 0., 0.])):
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

        #track info
        self.TID = 0
        self.velocity = None
        self.confidence = None

        # Tracking state
        # 0 -> OFF (object not valid)
        # 1 -> OK
        # 2 -> SEARCHING (occlusion occurred, trajectory is estimated)
        self.tracking_state = None

        # Action state
        # 0 -> IDLE
        # 2 -> MOVING
        self.action_state = None

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

    def setZedObjDetInfo(self, obj):
        self.TID = obj.label_id
        self.pos = numpy.array(list(obj.position))
        tpos = numpy.array(list(obj.position))
        #print(self.pos.dtype)
        #self.pos[:,[1, 0]] = self.pos[:,[0, 1]]
        self.pos[0] = tpos[0]
        self.pos[1] = tpos[1]
        #print(self.pos, self.pos.dtype)
        #self.size = obj.
        self.velocity = obj.velocity
        self.confidence = obj.confidence
        self.tracking_state = obj.tracking_state
        self.action_state = obj.action_state