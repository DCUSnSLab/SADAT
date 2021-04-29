from dadatype.dtype_cate import DataTypeCategory


class DataWrapper():
    __slots__ = ('id', 'posx', 'posy', 'dtypecate')
    def __init__(self, id, dtypecate):
        self.id = id
        self.dtypecate = dtypecate
        self.dataGroup = DataTypeCategory.checkGroupType(self.dtypecate)

    def __metertoPixel(self):
        pass