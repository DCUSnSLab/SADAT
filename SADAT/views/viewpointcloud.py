import math
from views.DataView import DataView
import numpy as np

class viewPointCloud(DataView):
    def __init__(self, pdata=None):
        super().__init__(rawdata=pdata)
        self.colorrange = list()

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()


    def drawIndividual(self,qp,xp,yp,ikey):
        qp.drawEllipse(xp,yp,6,6)


    def draw3DVisual(self, pos, ikey):
        color = pos[:,3:7]

        return pos, color