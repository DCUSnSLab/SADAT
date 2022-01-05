from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDockWidget, QGroupBox, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QGridLayout, \
    QTreeWidget, QTreeWidgetItem

from gui.guiVehicleInfoTree import vehicleInfoTree


class SideDock(QDockWidget):
    def __init__(self, parent):
        super().__init__('sideDock', parent)
        self.parent = parent
        self.width = 300

        self.initUI()

    def initUI(self):

        # Vehicle Control
        self.StopBtn = QPushButton("STOP")
        self.StopBtn.setMaximumSize(100, 50)

        self.vControlLayout = QVBoxLayout()
        self.vControlLayout.addWidget(self.StopBtn)

        self.vehicleControl = QGroupBox("Vehicle Control")
        self.vehicleControl.setStyleSheet("color:black;"
                                          "background-color:white;")
        self.vehicleControl.setLayout(self.vControlLayout)


        self.vinfoTree = vehicleInfoTree(self)
        self.vInfoLayout = QVBoxLayout()
        self.vInfoLayout.addWidget(self.vinfoTree)
        self.vInfoLayout.setAlignment(Qt.AlignTop)

        self.vInfoLaBox = QGroupBox("Vehicle Info")
        self.vInfoLaBox.setStyleSheet("color:black;"
                                      "background-color: white")
        self.vInfoLaBox.setLayout(self.vInfoLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.vehicleControl, 10)
        self.mainLayout.addWidget(self.vInfoLaBox, 90)

        #set Main Widget
        self.mainWidget = QGroupBox()
        self.mainWidget.setStyleSheet("color:black;"
                                      "background-color:white;")
        self.mainWidget.setLayout(self.mainLayout)
        #self.mainWidget.setFixedWidth(self.width)
        self.setWidget(self.mainWidget)
        self.setFloating(False)