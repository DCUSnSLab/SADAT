from dadatype.datawrapper import DataWrapper


class dtype_rplidar(DataWrapper):
    def __init__(self, posx=0, posy=0, startflag=0):
        super().__init__(posx, posy)
        self.startflag = startflag