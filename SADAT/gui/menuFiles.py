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

class menuLoadSim(QAction,QWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        #self.triggered.connect(self.trig)
        self.triggered.connect(self.OnOpenDocument)
        self.setShortcut('Ctrl+S')
        self.setStatusTip('Exit application')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_SIM)
        print("PlaySim")

    def OnOpenDocument(self):
        print('connect')
        fname = QFileDialog.getOpenFileName(self,'Open file','/Users/yuri/SADAT/Data')

        #self.trig
        print(fname)

class menuLoadSim_pcd(QAction, QWidget):
    def __init__(self, name, parent):
        print("name")
        print(name)
        print("parent")
        print(parent)
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        #self.triggered.connect(self.OnOpenDocument)
        #self.setStatusTip('Exit application')

    def trig(self):
        print("Clicked Test")
        #fname = QFileDialog.getOpenFileName(self)
        #print(fname[0])

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



