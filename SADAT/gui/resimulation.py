from PyQt5.QtWidgets import QAction, QDialog, QPlainTextEdit, QGridLayout, QLabel, QPushButton, QFileDialog, QComboBox
from PyQt5.QtGui import *
import rosbag

class reSimulation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.simulator = self.parent.simulator

        self.filename = ""

        self.setWindowTitle('ReSimulation')
        self.setGeometry(300, 300, 300, 200)
        self.show()
        self.initUI()

    def initUI(self):

        # rosbag file open UI

        self.text1 = QPlainTextEdit('Published Topics')
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)

        self.openbagfile = QPushButton('File', self)
        self.openbagfile.clicked.connect(self.loadbagfile)

        self.gridlayout.addWidget(self.openbagfile, 0, 0)
        self.gridlayout.addWidget(QLabel(self.filename), 0, 1)

        # Algorithm Category UI

        self.algocate = QComboBox(self)

        self.algocate.addItem("Algo Category 1")
        self.algocate.addItem("Algo Category 2")
        self.algocate.addItem("Algo Category 3")
        self.algocate.addItem("Algo Category 4")

        self.gridlayout.addWidget(QLabel('Algorithm Category : '), 1, 0)
        self.gridlayout.addWidget(self.algocate, 1, 1)

        # Implemented Algorithm UI

        self.algolist = QComboBox(self)

        self.algolist.addItem("Algo 1")
        self.algolist.addItem("Algo 2")
        self.algolist.addItem("Algo 3")
        self.algolist.addItem("Algo 4")

        self.gridlayout.addWidget(QLabel('Test Algorithm : '), 2, 0)
        self.gridlayout.addWidget(self.algolist, 2, 1)

        # Resimulation execute

        self.resimulate = QPushButton('Resim', self)
        self.resimulate.clicked.connect(self.resimulation)
        self.gridlayout.addWidget(self.resimulate, 3, 0)

        # Resim Visualization UI

    def loadbagfile(self):
        # print("loadbagfile")
        self.filename = QFileDialog.getOpenFileName(self, 'Open rosbag file', '/home/ros/rosbag')[0]
        print(self.filename)

    def resimulation(self):
        print("resimulation")
        self.bag_file = rosbag.Bag(self.filename)
        print("load bag file")

        read_topic = '/velodyne_points'

        for topic, msg, t in self.bag_file.read_messages(read_topic):
            print(t)
            print(msg.header)