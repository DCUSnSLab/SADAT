from views.DataView import DataView

class viewLine(DataView):
    def __init__(self,lidata=None):
        super().__init__(rawdata=lidata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def drawIndividual(self,qp, xp, yp, ikey):
        for tdata in self.pos_xy:
            xp=int(tdata[0])
            yp=int(tdata[1])

            qp.drawLine(xp,yp,10,10)