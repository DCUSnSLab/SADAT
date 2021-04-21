import copy

from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class grp_rplidar(DataWrapper):
    def __init__(self, pnt, distance, angle, timestamp=0, start_flag=False):
        super().__init__(id=0, dtypecate=DataTypeCategory.POINT_CLOUD)
        self.__timestamp = timestamp
        self.__pntxy = pnt
        self.__distance = distance
        self.__angle = angle
        self.__start_flag = start_flag

    def getTimeStamp(self):
        return self.__timestamp

    def getPoints(self):
        return self.__pntxy

    # def getPosX(self):
    #     return self.__pntxy[1]
    #
    # def getPosY(self):
    #     return self.__pntxy[2]

    def getStartFlag(self):
        return self.__start_flag

    def clone(self, obj):
        if obj != None:
            self.__timestamp = obj.getTimeStamp()
            self.__start_flag = obj.getStartFlag()
            self.__pntxy = copy.deepcopy(obj.getPoints())