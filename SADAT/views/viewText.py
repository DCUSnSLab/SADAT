from views.DataView import DataView

class viewTrack(DataView):
    def __init__(self, txdata=None):
        super().__init__(rawdata=txdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def Textdraw(self,qp, xp, yp, ikey):
        qp.drawText(xp,yp,10,10)

