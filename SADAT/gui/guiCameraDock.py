from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QDockWidget


class cameraDock(QDockWidget):
    def __init__(self):
        super().__init__('Camera Window')
        self.cwidth = 300
        self.pixmap = None
        #self.setStyleSheet("color:black;background-color:white;")
        self.label = QLabel(self)
        self.label.setContentsMargins(0,0,0,0)
        self.label.setGeometry(0,30,self.cwidth,self.cwidth*0.5624)
        #self.label.setFixedSize(self.cwidth, 300)
        self.label.setMinimumSize(QSize(1, 1))
        #self.label.setStyleSheet("background-color:black;")

        self.setFloating(True)

    def minimumSizeHint(self) -> QSize:
        return QSize(self.cwidth, 110)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.scalePixmap()

    def setPixmap(self, pm):
        self.pixmap = QPixmap.fromImage(pm)
        self.scalePixmap()

    def scalePixmap(self):
        if self.pixmap is not None:
            #self.resize(self.width(), self.height())
            self.pixmap = self.pixmap.scaled(self.width(), self.height()-30, Qt.KeepAspectRatio)
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.width(), self.height()-30)
