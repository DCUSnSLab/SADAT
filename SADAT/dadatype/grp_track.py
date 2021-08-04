import copy
from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class grp_pointclouds(DataWrapper):
    def __init__(self, tracks=None, timestamp=0):
        super().__init__(id=0, dtypecate=DataTypeCategory.POINT_CLOUD, timestamp=timestamp)
        self.__tracks = tracks


    def getTimeStamp(self):
        return self.__timestamp

    def getTracks(self):
        return self.__tracks

    def addTracks(self, track):
        self.__tracks = track

    def clone(self, obj):
        if obj != None:
            self.__timestamp = obj.getTimeStamp()
            self.__start_flag = obj.getStartFlag()
            self.__pntxy = copy.deepcopy(obj.getPoints())