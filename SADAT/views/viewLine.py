from views.DataView import DataView

class viewLine(DataView):
    def __init__(self,lidata=None):
        super().__init__(rawdata=lidata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def drawIndividual(self,qp, xp, yp, ikey):
        qp.drawLine(xp,yp,10,10)