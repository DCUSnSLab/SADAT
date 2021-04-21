import datetime as pydatetime
from GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class GrabberROSCam(GrabberROS):
    def __init__(self, _log):
        super().__init__(_log, AttachedSensorName.USBCAM, 'usbCamGrabber')
        self.selecting_sub_image = "compressed"  # you can choose image type "compressed", "raw"

        if self.selecting_sub_image == "compressed":
            self._topicName = '/usb_cam/image_raw/compressed'
        else:
            self._topicName = '/usb_cam/image_raw'

        self._initMsgType()

        print(self.rospy.get_published_topics())

    def userCallBack(self, msg):
        self.sendData(msg)
