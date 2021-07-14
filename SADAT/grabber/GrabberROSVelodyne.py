import datetime as pydatetime
from grabber.GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer
import time


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class GrabberROSVelodyne(GrabberROS):
    def __init__(self, disp):
        super().__init__(disp, [AttachedSensorName.VelodyneVLC16], 'VelodyneGrabber', 'velodyne_points')
        self.prevTime = 0

    def userCallBack(self, msgs):
        #send to LogPlayDispatcher
        #print(msgs[0])
        curTime = time.time()
        sec = curTime - self.prevTime
        self.prevTime = curTime
        fps = 1 / (sec)
        #print('velo fps -',fps)
        self.sendData(msgs[0])
