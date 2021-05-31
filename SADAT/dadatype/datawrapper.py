from dadatype.dtype_cate import DataTypeCategory
import numpy as np

class DataWrapper():
    __slots__ = ('id', 'posx', 'posy', 'posz', 'dtypecate')
    def __init__(self, id, dtypecate):
        self.id = id
        self.dtypecate = dtypecate
        self.dataGroup = DataTypeCategory.checkGroupType(self.dtypecate)

    def __metertoPixel(self):
        pass

    def getPoints(self):
        return np.array([self.posx, self.posy, self.posz])