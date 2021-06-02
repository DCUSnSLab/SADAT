from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
from numpy import inf
import numpy as np
from log.makeRPLidarLog import RPLidarLogType
import math
import datetime as pydatetime


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class RPLidar2DA3(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.RPLidar2D, name)

    def _doWorkDataInput(self, msg):
        # print(len(msg.ranges))
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_inc = msg.angle_increment
        # print(angle_min, angle_max, angle_inc)
        cnt = 0

        rpdata = RPLidarLogType()
        distance = list()
        angle = list()
        timestamp = 0

        for data in msg.ranges:
            range = data
            if data == inf:
                range = 0
            rosdata = self.makeDatafromROS(math.degrees(angle_min + (angle_inc * cnt)), range * 1000, cnt,
                                           get_now_timestamp())
            distance.append(rosdata['distance'])
            angle.append(rosdata['angle'])
            timestamp = rosdata['timestamp']
            cnt += 1

        rpdata.distance = np.array(distance)
        rpdata.angle = np.array(angle)
        rpdata.timestamp = timestamp
        rpdata.start_flag = True

        tempX, tempY = self._inputdataArray(rpdata)
        X_Y = np.array([(tempX[i], tempY[i], 0) for i in range(len(tempX))], dtype=np.float32)

        lgrp = grp_rplidar(X_Y, rpdata.distance, rpdata.angle, rpdata.timestamp, rpdata.start_flag)
        if len(lgrp.getPoints()) == 0:
            print('inSensor - ', lgrp.getPoints())
            print('lgrp is None',lgrp.getTimeStamp())

        self.addRealtimeData(lgrp)