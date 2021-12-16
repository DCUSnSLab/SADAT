from views.DataView import DataView

class viewTrack(DataView):
    def __init__(self, txdata=None):
        super().__init__(rawdata=txdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def _getPos(self):
        return None

    def _getSize(self):
        return None

    def _getColor(self):
        return None

    def drawIndividual(self,qp,xp,yp,ikey):
        qp.drawText(xp,yp,10,10)

