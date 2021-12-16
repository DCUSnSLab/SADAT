from abc import *

import numpy


class DataView(metaclass=ABCMeta):
    def __init__(self, rawdata=None):
        self.rawdata = rawdata
        self.rawid = -1
        self.isVisible = True
        self.viewType = None
        self.viewGroup = None

        self.pos_xy = None
        self.size = None
        self.color = None

    def initView(self, rdata):
        self.viewType = rdata.dtypecate
        self.viewGroup = rdata.dataGroup
        self.addRawData(rdata)

    def addRawData(self, rdata):
        self.rawdata = rdata
        self.rawid = self.rawdata.id

    def updatePlanviewPos(self):
        #self.guiinfo = guiinfo
        self.pos_xy = self._getPos()
        self.size = self._getSize()
        self.color = self._getColor()
        self._updatePlanviewSub()


    def _updatePlanviewSub(self):
        pass

    def draw(self, ikey, gl=False, qp=None):
        if self.isVisible:
            if gl is True:
                return self.draw3DVisual()
            else:
                for tdata in self.pos_xy:
                    xp=int(tdata[0])
                    yp=int(tdata[1])
                    self.drawIndividual(qp,xp,yp,ikey)
        else:
            return (None, None, None)

    def draw3DVisual(self):
        return self.pos_xy, self.size, self.color

    @abstractmethod
    def drawIndividual(self,qp,xp,yp,ikey):
        pass

    @abstractmethod
    def _getPos(self):
        pass

    @abstractmethod
    def _getSize(self):
        pass

    @abstractmethod
    def _getColor(self):
        pass

    # def _getSize(self, w, h):
    #     w = w / self.guiinfo.planviewsize
    #     h = h / self.guiinfo.planviewsize
    #     return w,h

    def setVisible(self,tf):
        self.isVisible=tf