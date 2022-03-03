from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QToolBar, QLabel, QPushButton

from gui.comboCheck import CheckableComboBox
from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer


class toolbarPlanviewVisible(QToolBar):
    def __init__(self, parent):
        super().__init__('Visible',parent=parent)
        self.parent = parent
        self.initUI()

        #for planview btn
        self.is3d = True
        self.initPlanviewUI()


    def initUI(self):
        self.title = QLabel('Object Visible  ')
        self.cb = CheckableComboBox()
        self.cb.setFixedHeight(30)
        self.cb.setFixedWidth(200)

        self.addWidget(self.title)
        self.addWidget(self.cb)


    def initPlanviewUI(self):
        self.pvbtn = QPushButton('Convert 2D Planview')

        if Importer.checkVispy() is False:
            self.is3d = False
            self.pvbtn.setVisible(False)

        self.pvbtn.clicked.connect(self.pvbtnClicked)
        self.addWidget(self.pvbtn)


    def pvbtnClicked(self):
        if self.is3d is True:
            self.parent.setPlanviewWidget(1)
            self.pvbtn.setText('Convert 3D Planview')
            self.is3d = False
        else:
            self.parent.setPlanviewWidget(0)
            self.pvbtn.setText('Convert 2D Planview')
            self.is3d = True

    def refreshList(self, objs):
        self.cb.refreshList(objs)