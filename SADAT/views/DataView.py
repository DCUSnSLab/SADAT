class DataView:
    def __init__(self, rawdata=None):
        self.rawdata = rawdata
        self.isVisible = True
        self.viewType = None

        self.guiinfo = None
        self.pos_xy = list()

    def initView(self, rdata):
        self.viewType = rdata.dtypecate
        self.addRawData(rdata)

    def addRawData(self, rdata):
        self.rawdata = rdata

    def updatePlanviewPos(self, guiinfo):
        self.pos_xy.clear()
        self.guiinfo = guiinfo
        if self.viewType.name != 'POINT_CLOUD':
            posxy = self._getPos(self.rawdata.posx, self.rawdata.posy)
            self.pos_xy.append(posxy)
        else:
            self.pos_xy = [self._getPos(pntdata[0],pntdata[1]) for pntdata in self.rawdata.getPoints()]

        self._updatePlanviewSub()

    def _updatePlanviewSub(self):
        pass

    def draw(self, ikey, gl=None, qp=None):
        if self.isVisible:
            if gl is not None:
                print(type(self.rawdata.getPoints()))
                return None
                #self.drawPyqtGraph()
            else:
                for tdata in self.pos_xy:
                    xp=int(tdata[0])
                    yp=int(tdata[1])
                    self.drawIndividual(qp,xp,yp,ikey)


    def drawPyqtGraph(self, pos, ikey, gl):
        pass

    def drawIndividual(self,qp,xp,yp,ikey):
        pass

    def _getPos(self, posx, posy):
        rposx = (posx / self.guiinfo.planviewsize) + (self.guiinfo.wwidth / 2) + self.guiinfo.relx
        rposy = (posy / self.guiinfo.planviewsize) + (self.guiinfo.wheight / 2) + self.guiinfo.rely

        return rposx, rposy

    def _getSize(self, w, h):
        w = w / self.guiinfo.planviewsize
        h = h / self.guiinfo.planviewsize
        return w,h

    def setVisible(self,tf):
        self.isVisible=tf
