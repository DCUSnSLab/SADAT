from views.DataView import DataView

class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def drawIndividual(self,qp, xp, yp, ikey):
        for tdata in self.pos_xy:
            xp=int(tdata[0])
            yp=int(tdata[1])

            qp.drawRect(xp,yp,10,10)

