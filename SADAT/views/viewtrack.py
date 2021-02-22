from views.DataView import DataView
from PyQt5.QtGui import *

class viewTrack(DataView):
    def __init__(self, tdata=None):
        super().__init__(rawdata=tdata)

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()

    def drawIndividual(self,qp, xp, yp, ikey):
        for tdata in self.pos_xy:
            xp = int(tdata[0])
            yp = int(tdata[1])

            color = QColor()
            color.setNamedColor(self.rawdata.color)
            qp.setPen(color)

            # 생성된 군집 id 출력
            qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2), "Cluster_" + str(self.rawdata.id))
            # 생성된 군집 중심좌표까지의 거리 출력
            qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2) + 20,
                        "distance : " + format(self.rawdata.distance, ".2f") + "m")
            qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2) + 40,
                        "Width, Height : " + format((self.rawdata.meterWidth), ".2f") + "m " + format((self.rawdata.meterHeight), ".2f") + "m")
            qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2) + 60,
                        "Area : " + format(self.rawdata.squareMeterArea, ".2f") + "m^2")
            qp.drawText(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2) + 80,
                        "Speed : " + format(self.rawdata.speed, ".2f") + "m/s")
            qp.drawRect(xp - int((self.rawdata.width / self.guiinfo.planviewsize) / 2),
                        yp - int((self.rawdata.height / self.guiinfo.planviewsize) / 2),
                        int(self.rawdata.width / self.guiinfo.planviewsize), int(self.rawdata.height / self.guiinfo.planviewsize))

            # qp.drawRect(xp,yp,10,10)