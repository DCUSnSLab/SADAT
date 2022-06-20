import pcl
import numpy as np
import pcl.pcl_visualization

import sys
from PyQt5.QtWidgets import *

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

def main():
    cloud = pcl.load("../../../20211028_map.pcd")
    # cloud = pcl.load("../../../bunny.pcd")
    pc = PointCloud()
    pc2 = PointCloud2()

    # Centred the data
    centred = cloud - np.mean(cloud, 0)
    ptcloud_centred = pcl.PointCloud()
    ptcloud_centred.from_array(centred)

    visual = pcl.pcl_visualization.CloudViewing()

    # PointXYZ
    visual.ShowMonochromeCloud(ptcloud_centred, b'cloud')
    v = True
    while v:
        v = not(visual.WasStopped())

if __name__ == "__main__":
    main()
    #app = QApplication(sys.argv)
    #window = MyWindow()
    #window.show()
    #app.exec_()