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
        try:
            self.bridge = Importer.importerLibrary('cv_bridge','CvBridge')
        except:
            self.bridge = None

        self.prevTime = 0
        self.selecting_sub_image = "compressed"  # you can choose image type "compressed", "raw"

    def _doWorkDataInput(self, msg):
        try:
            if self.bridge is None:
                pass

            cv_image = None
            inputdata = msg

            if self.selecting_sub_image == "compressed":
                # converting compressed image to opencv image
                np_arr = np.fromstring(msg.data, np.uint8)
                cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            elif self.selecting_sub_image == "raw":
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            curTime = time.time()
            sec = curTime - self.prevTime
            self.prevTime = curTime
            fps = 1 / (sec)
            tstamp = float(inputdata.header.stamp.to_sec())
            #print(tstamp.to_sec(), type(tstamp))
            h, w, ch = cv_image.shape
            str = "FPS : %0.1f %0.3f, res : %d %d" % (fps, tstamp, w, h)
            cv2.putText(cv_image, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #cv_image = cv2.resize(cv_image, dsize=(960,540), interpolation=cv2.INTER_CUBIC)

            # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            # result,cv_image = cv2.imencode('.jpg',cv_image,encode_param)

            #print(str)
            #h, w, ch = cv_image.shape
            #self.addRealtimeData(dtype_camera(cv_image))
            self.addRealtimeData(dtype_camera(cv_image, tstamp))
            #bytesPerLine = ch * w
            # convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_BGR888)
            # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            # self.signal.emit(convertToQtFormat)

            #cv2.imshow('cv_gray', cv_image), cv2.waitKey(1)
        except Exception as e:
            print(e)
        # tempX, tempY = self._inputdataArray(inputdata)
        # X_Y = np.array([(tempX[i], tempY[i]) for i in range(len(tempX))])
        # lgrp = grp_pointclouds(X_Y, inputdata.distance, inputdata.angle, inputdata.timestamp, inputdata.start_flag)
        # if len(lgrp.getPoints()) == 0:
        #     print('inSensor - ', lgrp.getPoints())
        #     print('lgrp is None',lgrp.getTimeStamp())

        # self.addRealtimeData(lgrp)