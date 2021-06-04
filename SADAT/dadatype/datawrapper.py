from dadatype.dtype_cate import DataTypeCategory
import numpy as np

class DataWrapper():
    __slots__ = ('id', 'posx', 'posy', 'posz', 'dtypecate')

    def __init__(self, id, dtypecate, timestamp=0):
        self.id = id
        self.dtypecate = dtypecate
        self.dataGroup = DataTypeCategory.checkGroupType(self.dtypecate)
        self._timestamp = timestamp

    def __metertoPixel(self):
        pass

    def getPoints(self):
        return np.array([self.posx, self.posy, self.posz])

    def getTimeStamp(self):
        return self._timestamp