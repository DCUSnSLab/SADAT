from views.DataView import DataView


class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)