from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory

class dtype_float(DataWrapper):
    def __init__(self, data):  # timestamp 추가 하면 추가됨
        super().__init__(id=0, dtypecate=DataTypeCategory.Float)  # , timestamp=timestamp)
        self.speed(data)
        self.position(data)

    def speed(self, speedfloat):
        self.speedfloat = speedfloat

    def position(self, positionfloat):
        self.positionfloat = positionfloat

class dtype_sensor(DataWrapper):
    def __init__(self, data):
        super().__init__(id=0, dtypecate=DataTypeCategory.Sensor)
        self.imudata(data)

    def imudata(self,imusensor):
        self.imusensor = imusensor

class dtype_Odometry(DataWrapper):
    def __init__(self, odometrydata):
        super().__init__(id=0, dtypecate=DataTypeCategory.Odometry)
        self.odometrydata = odometrydata
