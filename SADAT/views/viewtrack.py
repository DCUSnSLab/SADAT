from views.DataView import DataView

class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def Trackdraw(self,qp,xp,yp,ikey):
        #color.setNamedColor(idata.rawdata.color)
        #qp.setPen(color)

        # 생성된 군집 id 출력
        qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                    yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2), "Cluster_" + str(self.rawdata.id))
        # 생성된 군집 중심좌표까지의 거리 출력
        qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                    yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2) + 20, "distance : " + str(self.rawdata.distance))
        qp.drawRect(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                    yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2),
                    int(self.rawdata.width / self.guiinfo.planviewsize), int(self.rawdata.height / self.guiinfo.planviewsize))

        # qp.drawRect(xp,yp,10,10)