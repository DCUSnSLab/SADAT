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


    def _getPos(self):
        return self.rawdata.getPoints()

    def _getSize(self):
        return None

    def _getColor(self):
        return self.pos_xy[:, 3:7]