from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_tracker(DataWrapper):
    def __init__(self, id, minX, maxX, minY, maxY, posx, posy, width, height, distance, acc, speed, color = "#ffffff"):
        super().__init__(id=id, posx=posx, posy=posy, dtypecate=DataTypeCategory.TRACK)
        self.ref_point = 0

        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

        self.distance = distance
        self.width = width
        self.height = height

        self.meterWidth = self.width / 1000
        self.meterHeight = self.height / 1000
        self.squareMeterArea = self.meterWidth * self.meterHeight

        self.acc = acc
        self.speed = speed
        self.color = color
