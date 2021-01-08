from dadatype.datawrapper import DataWrapper


class dtype_tracker(DataWrapper):
    def __init__(self, id, posx=0, posy=0, width=0, height=0):
        super().__init__(posx=posx, posy=posy, id=id)
        self.ref_point = None
        self.width = None
        self.height = None
        self.acc = None
        self.speed = None