from views.DataView import DataView

class viewLane(DataView):
    def __init__(self,ldata=None):
        super().__init__(rawdata=ldata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def _getPos(self):
        return None

    def _getSize(self):
        return None

    def _getColor(self):
        return None

    def drawIndividual(self,qp,xp,yp,ikey):
        qp.drawLine(xp,yp,6,6)