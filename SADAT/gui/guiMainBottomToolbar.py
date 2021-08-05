from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QToolBar, QLabel

from gui.comboCheck import CheckableComboBox
from sensor.SenAdptMgr import AttachedSensorName


class toolbarPlanviewVisible(QToolBar):
    def __init__(self, parent):
        super().__init__('Visible',parent=parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.title = QLabel('Object Visible  ')
        self.cb = CheckableComboBox()
        self.cb.setFixedHeight(30)
        self.cb.setFixedWidth(200)

        self.addWidget(self.title)
        self.addWidget(self.cb)
    def refreshList(self, objs):
        self.cb.refreshList(objs)