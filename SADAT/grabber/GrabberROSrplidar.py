from grabber.GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName

class GrabberROSrplidar(GrabberROS):
    def __init__(self, disp):
        super().__init__(disp, [AttachedSensorName.RPLidar2DA3], 'LidarGrabber', 'scan')

    def userCallBack(self, msgs):
        msg = msgs[0]


        #send to LogPlayDispatcher
        self.sendData(msg)
