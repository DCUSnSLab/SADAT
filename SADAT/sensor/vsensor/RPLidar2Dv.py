from time import time

#from dadatype.dtype_rplidar import dtype_rplidar
from dadatype.dtype_test import dtype_test
from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor
import numpy as np

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
            X_Y = [(tempX[i]*0.001, tempY[i]*0.001, 0, 1, 1, 1, 1) for i in range(len(tempX))]
            X_Y_n = np.array(X_Y)
            lgrp = grp_rplidar(X_Y_n, rdata.distance, rdata.angle, rdata.timestamp[0], rdata.start_flag[0])

            self._addSimData(lgrp)

            # tempXY.append(tempX)
            # tempXY.append(tempY)
            # tempXY.append(rdata.timestamp[0])
            # tempXY.append(rdata.start_flag[0])
            # self._addSimData(tempXY)