import copy

from dadatype.dtype_cate import DataTypeCategory


class grp_rplidar():
    def __init__(self, timestamp=0, pnt=None, start_flag=False):
        self.__timestamp = timestamp
        self.__pntxy = pnt
        self.__start_flag = start_flag
        self.dtypecate = DataTypeCategory.POINT_CLOUD

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
        self.__timestamp = obj.getTimeStamp()
        self.__start_flag = obj.getStartFlag()
        self.__pntxy = copy.deepcopy(obj.getPoints())