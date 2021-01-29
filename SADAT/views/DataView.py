from externalmodules.default.dataset_enum import senarioBasicDataset

class DataView:
    def __init__(self, rawdata=None):
        self.rawdata = rawdata
        self.isVisible = False
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
            posxy = self.__getPos(self.rawdata.posx, self.rawdata.posy)
            self.pos_xy.append(posxy)
        else:
            self.pos_xy = [self.__getPos(px, py) for idx, px, py in self.rawdata.getPoints()]

    def _draw(self, qp, xp, yp, ikey):
        if ikey is senarioBasicDataset.TRACK:
            qp.drawRect(xp, yp, 10, 10)
        else:
            qp.drawEllipse(xp, yp, 6, 6)

    def __getPos(self, posx, posy):
        rposx = (posx / self.guiinfo.planviewsize) + (self.guiinfo.wwidth / 2) + self.guiinfo.relx
        rposy = (posy / self.guiinfo.planviewsize) + (self.guiinfo.wheight / 2) + self.guiinfo.rely

        return rposx, rposy
