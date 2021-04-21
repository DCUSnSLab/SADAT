from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_tracker(DataWrapper):
    def __init__(self, id, minX, maxX, minY, maxY, posx, posy, subX, subY, distance, color = "#ffffff"):
        super().__init__(id=id, dtypecate=DataTypeCategory.TRACK)
        self.posx = posx
        self.posy = posy

        self.ref_point = 0

        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

        self.distance = distance
        # 변수명 변경 필요
        # width -> subX, height -> subY
        self.width = subX
        self.height = subY

        self.acc = 0
        self.speed = 0

        self.color = color
