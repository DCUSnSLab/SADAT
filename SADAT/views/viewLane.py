from views.DataView import DataView

class viewLane(DataView):
    def __init__(self,ldata=None):
        super().__init__(rawdata=ldata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()
    def drawIndividual(self,qp, xp, yp, ikey):
        for tdata in self.pos_xy:
            xp=int(tdata[0])
            yp=int(tdata[1])

            qp.drawLine(xp,yp,6,6)