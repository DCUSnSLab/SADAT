from dadatype.dtype_camera import dtype_camera
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import time
import cv2
import numpy as np

from utils.importer import Importer


class USBCAM(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Camera, name)
        self.bridge = Importer.importerLibrary('cv_bridge','CvBridge')
        self.prevTime = 0
        self.selecting_sub_image = "compressed"  # you can choose image type "compressed", "raw"

    def _doWorkDataInput(self, inputdata):
        try:
            if self.selecting_sub_image == "compressed":
                # converting compressed image to opencv image
                np_arr = np.fromstring(inputdata.data, np.uint8)
                cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
                #cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            elif self.selecting_sub_image == "raw":
                cv_image = self.bridge.imgmsg_to_cv2(inputdata, "bgr8")

            #cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

            curTime = time.time()
            sec = curTime - self.prevTime
            self.prevTime = curTime
            fps = 1 / (sec)
            tstamp = float(inputdata.header.stamp.to_sec())
            #print(tstamp.to_sec(), type(tstamp))
            str = "FPS : %0.1f %0.3f" % (fps, tstamp)
            cv2.putText(cv_image, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #print(str)
            h, w, ch = cv_image.shape
            #self.addRealtimeData(dtype_camera(cv_image))
            self.addRealtimeData(dtype_camera(cv_image))
            bytesPerLine = ch * w
            # convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_BGR888)
            # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            # self.signal.emit(convertToQtFormat)

            #cv2.imshow('cv_gray', cv_image), cv2.waitKey(1)
        except Exception as e:
            print(e)
        # tempX, tempY = self._inputdataArray(inputdata)
        # X_Y = np.array([(tempX[i], tempY[i]) for i in range(len(tempX))])
        # lgrp = grp_rplidar(X_Y, inputdata.distance, inputdata.angle, inputdata.timestamp, inputdata.start_flag)
        # if len(lgrp.getPoints()) == 0:
        #     print('inSensor - ', lgrp.getPoints())
        #     print('lgrp is None',lgrp.getTimeStamp())

        # self.addRealtimeData(lgrp)