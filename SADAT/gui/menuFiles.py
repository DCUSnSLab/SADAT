import os

import rosbag

from gui.guiROSManager import guiROSManager, LogStringHandler
from utils.sadatlogger import slog

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.menuItem import MenuItem
from simMode import Mode

class menuLoadSim(QAction):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        # self.triggered.connect(self.trig)

        self.logsteram = LogStringHandler
        self.triggered.connect(self.OepnFile)
        self.setShortcut('Ctrl+S')
        self.setStatusTip('Exit application')

    # def trig(self):
    #     self.parent.simulator.setAction(Mode.MODE_SIM)
    #     print("PlaySim")

    def OepnFile(self):
        print('connect')
        self.fileselect = QFileDialog.getOpenFileName(directory='../')
        self.file_info = self.fileselect[0]
        print(self.file_info)
        self.Topic_info()

    def Topic_info(self):
        self.rosmanager = guiROSManager(self.parent)
        self.test_bagfile = rosbag.Bag(self.file_info)
        self.topic_info = self.test_bagfile.get_type_and_topic_info()
        # for k in self.topic_info.topics.keys():
        #     print(k)
        print("test topic list")


        print("testtest",slog.addHandler(self.file_info))

        # for topic, msg, t in self.test_bagfile:
        #     print(topic)
        # if fileselect[0]:
        #     f = open(fileselect[0],)
        #     line = f.read()
        #     print(line)

class menuLogPlay(QAction):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+L')
        self.setStatusTip('Logging')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_LOG)
        self.parent.simulator.playMode()

class menuLogPlayROS(QAction):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+R')
        self.setStatusTip('Logging with ROS')

    def trig(self):
        # self.parent.simulator.setAction(Mode.MODE_LOG, Mode.LOGTYPE_ROS)
        # self.parent.simulator.playMode()
        self.rosmanager = guiROSManager(self.parent)



