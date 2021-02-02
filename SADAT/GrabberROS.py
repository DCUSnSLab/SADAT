import platform
import time
import datetime as pydatetime

import numpy

from LidarLog import LidarLog
from multiprocessing import Manager
import rospy
from sensor_msgs.msg import LaserScan
from numpy import inf
import math
from multiprocessing import Value

from log.makeRPLidarLog import RPLidarLogType
from sensor.SenAdptMgr import AttachedSensorName


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class GrabberROS:
    def __init__(self, _log):
        self.log = _log
        self.log.initLog(1000)
        self.pwm = 1000
        self.lidar = None
        self.node = "GrabberROS"
        self.Signal = Value('i', 0)
        self.senstype = AttachedSensorName.RPLidar2DA3

    def connect(self):
        pass

    def startGrab(self):
        print('start grab')
        self.log.initLog(self.pwm)
        if self.log is not None:
            self.connect()
            self.startLidar()
            self.disconnect()

    def startLidar(self):
        print('init ROS scan')
        rospy.init_node('SADAT_scanvalue')
        print('start lidar')
        sub = rospy.Subscriber('/scan', LaserScan, self.lidarcallback)
        rospy.spin()
        print('end')

    def lidarcallback(self, msg):
        # print(len(msg.ranges))
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_inc = msg.angle_increment
        #print(angle_min, angle_max, angle_inc)
        cnt = 0

        rpdata = RPLidarLogType()
        distance = list()
        angle = list()
        timestamp = 0

        for data in msg.ranges:
            range = data
            if data == inf:
                range = 0
            rosdata = self.log.makeDatafromROS(math.degrees(angle_min+(angle_inc * cnt)), range*1000, cnt, get_now_timestamp())
            distance.append(rosdata['distance'])
            angle.append(rosdata['angle'])
            timestamp = rosdata['timestamp']
            cnt += 1

        rpdata.distance = numpy.array(distance)
        rpdata.angle = numpy.array(angle)
        rpdata.timestamp = timestamp
        rpdata.start_flag = True
        senddata = {self.senstype:rpdata}
        self.log.enQueueDataNew(senddata)
        #print("callback",self.Signal.value)
        if self.Signal.value == 1:
            print("Set Signal 1")
            self.disconnectSignal()

    def disconnect(self):
        print("ROS Grappber disconnect", self.node)
        self.Signal.value = 1

    def disconnectSignal(self):
        rospy.signal_shutdown("reason")
        print('ROS Disconnected')
