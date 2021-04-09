from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np

class RPLidar2DA3(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.RPLidar2D, name)

    def _doWorkDataInput(self, inputdata):
        tempX, tempY = self._inputdataArray(inputdata)
        X_Y = np.array([(tempX[i], tempY[i]) for i in range(len(tempX))])
        lgrp = grp_rplidar(X_Y, inputdata.distance, inputdata.angle, inputdata.timestamp, inputdata.start_flag)
        if len(lgrp.getPoints()) == 0:
            print('inSensor - ', lgrp.getPoints())
            print('lgrp is None',lgrp.getTimeStamp())

        self.addRealtimeData(lgrp)