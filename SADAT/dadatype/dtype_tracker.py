from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_tracker(DataWrapper):
    def __init__(self, id, minX, maxX, minY, maxY, posx=0, posy=0, width=0, height=0):
        super().__init__(id=id, posx=posx, posy=posy, dtypecate=DataTypeCategory.TRACK)
        self.ref_point = 0
        self.width = width
        self.height = height
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.acc = 0
        self.speed = 0