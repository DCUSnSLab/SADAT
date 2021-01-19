class DataWrapper():
    __slots__ = ('id', 'posx', 'posy', 'dtypecate')
    def __init__(self, id, posx, posy, dtypecate):
        self.id = id
        self.dtypecate=dtypecate
        self.posx = posx
        self.posy = posy

    def __metertoPixel(self):
        pass