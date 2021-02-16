from time import time

from dadatype.dtype_rplidar import dtype_rplidar
from dadatype.dtype_test import dtype_test
from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor


class RPLidar2Dv(vSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.RPLidar2D, name)

    def _doWorkDataInput(self, inputdata=None):
        tempX = []
        tempY = []
        tempXY = []
        # cnt = 0
        # print(len(rawdata))
        for rdata in inputdata:
            tempX = []
            tempY = []

            tempX, tempY = self._inputdataArray(rdata)
            X_Y = [(i, tempX[i], tempY[i]) for i in range(len(tempX))]
            lgrp = grp_rplidar(rdata.timestamp[0], X_Y, rdata.start_flag[0])

            #lgrp.caldistance()
            self._addSimData(lgrp)

            # tempXY.append(tempX)
            # tempXY.append(tempY)
            # tempXY.append(rdata.timestamp[0])
            # tempXY.append(rdata.start_flag[0])
            # self._addSimData(tempXY)