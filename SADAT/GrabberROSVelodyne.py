import datetime as pydatetime
from GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class GrabberROSVelodyne(GrabberROS):
    def __init__(self, disp):
        super().__init__(disp, [AttachedSensorName.VelodyneVLC16], 'VelodyneGrabber', 'velodyne_points')

    def userCallBack(self, msgs):
        #send to LogPlayDispatcher
        #print(msgs[0])
        self.sendData(msgs[0])
