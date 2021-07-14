import cv2
import numpy as np
from grabber.GrabberROS import GrabberROS
from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer
from utils.sadatlogger import slog


class GrabberROSCam(GrabberROS):
    def __init__(self, _dispatcher):
        super().__init__(_dispatcher, [AttachedSensorName.USBCAM], 'usbCamGrabber', 'usb_cam/image_raw/compressed')
        self.bridge = Importer.importerLibrary('cv_bridge', 'CvBridge')
        self.selecting_sub_image = "compressed"  # you can choose image type "compressed", "raw"

        # if self.selecting_sub_image == "compressed":
        #     self._topicName = '/usb_cam/image_raw/compressed'
        # else:
        #     self._topicName = '/usb_cam/image_raw'
        #
        # self._initMsgType()

    def userCallBack(self, msgs):
        inputdata = msgs[0]
        try:
            if self.selecting_sub_image == "compressed":
                # converting compressed image to opencv image
                np_arr = np.fromstring(inputdata.data, np.uint8)
                cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
                #cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            elif self.selecting_sub_image == "raw":
                cv_image = self.bridge.imgmsg_to_cv2(inputdata, "bgr8")
            self.sendData((cv_image,inputdata))
        except Exception as e:
            print(e)