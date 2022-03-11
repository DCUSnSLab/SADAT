from dadatype.dtype_cate import DataTypeCategory, DataGroup
import numpy as np
from abc import *

class DataWrapper(metaclass=ABCMeta):
    __slots__ = ('id', 'posx', 'posy', 'posz', 'dtypecate')

    def __init__(self, id, dtypecate, timestamp=0, isgroupobject=False):
        self.id = id
        self.dtypecate = dtypecate
        self.dataGroup = DataTypeCategory.checkGroupType(self.dtypecate)
        self._timestamp = timestamp
        self.__isGrpObject = isgroupobject

    def __metertoPixel(self):
        pass

    def getTimeStamp(self):
        return self._timestamp

    def isPointCloud(self):
        return self.dataGroup == DataGroup.GRP_POINTCLOUD

    def isGroupObject(self):
        return self.__isGrpObject
