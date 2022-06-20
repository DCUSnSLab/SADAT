import pcl
import numpy as np
import pcl.pcl_visualization

import sys
import math
from PyQt5.QtWidgets import *

from utils.importer import Importer

from sensor_msgs.msg import PointCloud, PointCloud2

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("Test")

        self.pushButton = QPushButton('Open')
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        print("Set Text")
        self.label.setText(fname[0])
        cloud = pcl.load(fname[0])

        # Centred the data
        centred = cloud - np.mean(cloud, 0)
        ptcloud_centred = pcl.PointCloud()
        ptcloud_centred.from_array(centred)

        visual = pcl.pcl_visualization.CloudViewing()

        # PointXYZ
        visual.ShowMonochromeCloud(ptcloud_centred, b'cloud')
        v = True
        while v:
            v = not (visual.WasStopped())

def num_to_rgb(val, max_val=141):
    rgb = 255
    i = (val * 255 / max_val);
    r = math.sin(0.024 * i + 0) * 127 + 128
    g = math.sin(0.024 * i + 2) * 127 + 128
    b = math.sin(0.024 * i + 4) * 127 + 128
    return [r / rgb, g / rgb, b / rgb, 1]

def __make_colormap():
    res = 1
    maxval = 256
    cnt = maxval * res
    color = [i * (1 / res) for i in range(cnt)]
    #print(color)
    cmap = [num_to_rgb(color[i], maxval) for i in range(len(color))]
    return np.array(cmap)

def main():
    cloud = pcl.load_XYZI("Data/20211104_map.pcd")
    # cloud = pcl.load("../../../bunny.pcd")

    np_cloud = np.empty([cloud.width, 4], dtype=np.float32)
    np_cloud = np.asarray(cloud)
    np_cloud = cloud.to_array()

    cmap = __make_colormap()

    # points = np.zeros((pc.shape[0], 7)) # 원본 코드의 pc.shape[0]은 PointCloud의 Width를 의미한다.
    points = np.zeros((cloud.width, 7))

    points[:, 0] = np_cloud[:, 0]
    points[:, 1] = np_cloud[:, 1]
    points[:, 2] = np_cloud[:, 2]
    points[:, 3] = np_cloud[:, 3]

    # inten = cloud.sensor_origin[3].astype(np.int32) # 입력받은 데이터의 Intensity를 정수형 값으로 변환하여 가져온 뒤,
    # color = np.array([cmap[inten[i]] for i in range(len(inten))]) # 해당 값을 바탕으로 색상을 설정한다.
    # points[:, 3:7] = color[:, 0:4] # 획득한 색상 값 저장
    points[:, 3:7] = 0

if __name__ == "__main__":
    main()
    #app = QApplication(sys.argv)
    #window = MyWindow()
    #window.show()
    #app.exec_()