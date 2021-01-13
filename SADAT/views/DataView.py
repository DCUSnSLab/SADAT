class DataView:
    def __init__(self, rawdata=None):
        self.rawdata = rawdata
        self.isVisible = False
        self.viewType = None

        self.guiinfo = None
        self.posx = 0
        self.posy = 0

    def initView(self, rdata):
        self.addRawData(rdata)

    def addRawData(self, rdata):
        self.rawdata = rdata

    def updatePlanviewPos(self, guiinfo):
        self.guiinfo = guiinfo
        self.posx = (self.rawdata.posx / self.guiinfo.planviewsize) + (self.guiinfo.wwidth / 2) + self.guiinfo.relx
        self.posy = (self.rawdata.posy / self.guiinfo.planviewsize) + (self.guiinfo.wheight / 2) + self.guiinfo.rely