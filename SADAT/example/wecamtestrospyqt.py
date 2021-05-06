import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import time
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class cvThread(QThread):
    signal = pyqtSignal(QImage)

    def __init__(self, qt):
        super(cvThread, self).__init__(parent=qt)
        print('init')
        rospy.init_node('gray')
        self.prevTime = 0
        self.selecting_sub_image = "compressed"  # you can choose image type "compressed", "raw"

        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()
        print('init finished')

    def callback(self, image_msg):
        try:
            if self.selecting_sub_image == "compressed":
                # converting compressed image to opencv image
                np_arr = np.fromstring(image_msg.data, np.uint8)
                cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
                #cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            elif self.selecting_sub_image == "raw":
                cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
            #cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
            size = cv_image.nbytes
            curTime = time.time()
            sec = curTime - self.prevTime
            self.prevTime = curTime
            fps = 1 / (sec)
            tstamp = float(image_msg.header.stamp.to_sec())
            #print(tstamp.to_sec(), type(tstamp))
            str = "FPS : %0.1f %0.3f" % (fps, tstamp)
            cv2.putText(cv_image, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

            h, w, ch = cv_image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(cv_image.data, w, h, cv_image.strides[0], QImage.Format_BGR888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.signal.emit(convertToQtFormat)

            #cv2.imshow('cv_gray', cv_image), cv2.waitKey(1)
        except Exception as e:
            print(e)

    def run(self):
        rospy.spin()




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 1920
        self.height = 1080
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(2000, 1100)
        # create a label
        self.label = QLabel(self)
        self.label.resize(1920, 1080)

        self.show()
        time.sleep(1)
        th = cvThread(self)
        th.signal.connect(self.setImage)
        # th.changePixmap.connect(self.setImage)
        th.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())