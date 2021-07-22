from GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName
import numpy as np
from numpy import inf
import math
import datetime as pydatetime
from log.makeRPLidarLog import RPLidarLogType
import cv2

def get_now():
    return pydatetime.datetime.now()


def get_now_timestamp():
    return get_now().timestamp()

class deprecated_GrabberROSSync(GrabberROS):
    def __init__(self, disp):
        super().__init__(disp, [AttachedSensorName.RPLidar2DA3, AttachedSensorName.USBCAM], 'ROSSyncGrabber'
                         ,['scan', 'usb_cam/image_raw/compressed'])
        self.selecting_sub_image = "compressed"

    def userCallBack(self, msgs):
        self.doLidar(msgs[0])
        self.doCam(msgs[1])

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


    def doLidar(self, msg):
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

        # send to LogPlayDispatcher
        self.sendData(rpdata, AttachedSensorName.RPLidar2DA3)

    def doCam(self, inputdata):
        try:
            if self.selecting_sub_image == "compressed":
                # converting compressed image to opencv image
                np_arr = np.fromstring(inputdata.data, np.uint8)
                cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
                # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            elif self.selecting_sub_image == "raw":
                cv_image = self.bridge.imgmsg_to_cv2(inputdata, "bgr8")
            self.sendData((cv_image, inputdata), AttachedSensorName.USBCAM)
        except Exception as e:
            print('doCAM',e)