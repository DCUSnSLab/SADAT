from views.DataView import DataView

class viewLane(DataView):
    def __init__(self,ldata=None):
        super().__init__(rawdata=ldata)