from views.DataView import DataView

class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def _getPos(self):
        return self.rawdata.getPoint()

    def _getSize(self):
        return self.rawdata.getSize()

    def _getColor(self):
        return None

    def drawIndividual(self,qp,xp,yp,ikey):
        pass