from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory
import numpy as np

class dtype_rplidar(DataWrapper):
    __slots__ = ('id', 'posx', 'posy', 'posz')
    def __init__(self, id, posx=0.0, posy=0.0):
        super().__init__(id=id, posx=posx, posy=posy, dtypecate=DataTypeCategory.POINT_CLOUD)

    def getPoints(self):
        return np.array([self.posx, self.posy, self.posz])