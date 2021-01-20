from views.DataView import DataView


class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)
        self.width = 0
        self.height = 0

    def _updatePlanviewSub(self):
        self.width, self.height = self._getSize(self.rawdata.width, self.rawdata.height)
        a = 3
