import os

from gui.guiROSManager import guiROSManager
from utils.sadatlogger import slog

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QFileDialog, QWidget, QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.menuItem import MenuItem
from simMode import Mode

import time

class menuLoadSim(QAction):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        #self.triggered.connect(self.OnOpenDocument)
        self.setShortcut('Ctrl+S')
        self.setStatusTip('Exit application')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_SIM)

    def OnOpenDocument(self):
        print('connect')
        fname = QFileDialog.getOpenFileName(self,'Open file','/Users/yuri/SADAT/Data')

        #self.trig
        print(fname)

class menuLoadSim_pcd(QAction, QWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        #self.triggered.connect(self.OnOpenDocument)
        self.setShortcut('Ctrl+D')
        self.setStatusTip('Exit application')

    def trig(self):
        # 아래 함수의 경우 현재 상속받은 parent의 속성에 직접적으로 접근하여 파일명을 지정합니다.
        # lSimDispatcher의 setFilesrc 함수를 단계별로 호출할 수 있도록 simulator 객체 클래스(SystemManager 클래스)에 별도의 함수 정의가 필요합니다.
        fl = fileLoader()
        filename = fl.open()

        self.parent.simulator.procs[Mode.MODE_SIM].lSimDispatcher.setFilesrc(filename[0])
        print("File path :", filename[0])

        self.parent.simulator.setAction(Mode.MODE_SIM)

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

class fileLoader(QWidget):
    def __init__(self):
        super().__init__()

    def open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/ros/pcd_data')

        # self.trig
        print(fname)
        print("PlaySim")
        return fname



