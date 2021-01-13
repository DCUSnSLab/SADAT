class DataWrapper():
    def __init__(self, posx, posy, dtypecate, id=-1):
        self.id = id
        self.dtypecate=dtypecate
        self.posx = posx
        self.posy = posy

    def __metertoPixel(self):
        pass