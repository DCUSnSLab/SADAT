from views.DataView import DataView

class viewPointCloud(DataView):
    def __init__(self, pdata=None):
        super().__init__(rawdata=pdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def drawIndividual(self,qp, xp, yp, ikey):
        for tdata in self.pos_xy:
            xp=int(tdata[0])
            yp=int(tdata[1])

            qp.drawEllipse(xp,yp,6,6)