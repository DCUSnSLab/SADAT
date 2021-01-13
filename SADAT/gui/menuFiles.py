import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QFileDialog, QWidget
from PyQt5.QtGui import *
from gui.menuItem import MenuItem
from simMode import Mode

class menuLoadSim(QAction,QWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        #self.triggered.connect(self.OnOpenDocument)
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

class menuLogPlay(QAction):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+L')
        self.setStatusTip('Logging')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_LOG)
        print("PlayLogging")