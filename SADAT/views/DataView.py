class DataView:
    def __init__(self, rawdata=None):
        self.rawdata = rawdata
        self.rawid = -1
        self.isVisible = True
        self.viewType = None

        self.pos_xy = None

    def initView(self, rdata):
        self.viewType = rdata.dtypecate
        self.addRawData(rdata)

    def addRawData(self, rdata):
        self.rawdata = rdata
        self.rawid = self.rawdata.id

    def updatePlanviewPos(self):
        #self.guiinfo = guiinfo
        self.pos_xy = self._getPos(self.rawdata.getPoints())
        self._updatePlanviewSub()

    def _updatePlanviewSub(self):
        pass

    def draw(self, ikey, gl=False, qp=None):
        if self.isVisible:
            if gl is True:
                data = self.pos_xy
                return self.draw3DVisual(data, ikey)
            else:
                for tdata in self.pos_xy:
                    xp=int(tdata[0])
                    yp=int(tdata[1])
                    self.drawIndividual(qp,xp,yp,ikey)
        else:
            return (None, None)


    def draw3DVisual(self, pos, ikey):
        return pos, None

    def drawIndividual(self,qp,xp,yp,ikey):
        pass

    def _getPos(self, points):
        return points#  * [0.01, 0.01, 0.01]

    # def _getSize(self, w, h):
    #     w = w / self.guiinfo.planviewsize
    #     h = h / self.guiinfo.planviewsize
    #     return w,h

    def setVisible(self,tf):
        self.isVisible=tf