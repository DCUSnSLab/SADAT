from dadatype.datawrapper import DataWrapper


class dtype_rplidar(DataWrapper):
    def __init__(self, id, posx=0.0, posy=0.0, startflag=False):
        super().__init__(posx=posx, posy=posy, id=id)