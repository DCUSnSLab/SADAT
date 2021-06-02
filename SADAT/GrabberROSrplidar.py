from GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName

class GrabberROSrplidar(GrabberROS):
    def __init__(self, disp):
        super().__init__(disp, [AttachedSensorName.RPLidar2DA3], 'LidarGrabber', 'scan')

    def makeDatafromROS(self, angle, range, cnt, timestamp):
        data = {}
        if cnt == 0:
            data['start_flag'] = True
        else:
            data['start_flag'] = False

        data['quality'] = None
        data['angle'] = angle
        data['distance'] = range
        data['timestamp'] = timestamp
        return data

    def userCallBack(self, msgs):
        msg = msgs[0]


        #send to LogPlayDispatcher
        self.sendData(msg)
