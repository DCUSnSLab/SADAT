from PyQt5.QtWidgets import QAction, QDialog, QPlainTextEdit, QGridLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import *

class reSimulation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.simulator = self.parent.simulator

        self.filename = None

        self.setWindowTitle('ReSimulation')
        self.setGeometry(300, 300, 300, 200)
        self.show()
        self.initUI()

    def initUI(self):
        self.text1 = QPlainTextEdit('Published Topics')
        self.gridlayout = QGridLayout()
        self.setLayout(self.gridlayout)

        self.openbagfile = QPushButton('File', self)
        self.openbagfile.clicked.connect(self.loadbagfile)

        self.gridlayout.addWidget(self.openbagfile, 0, 0)
        self.gridlayout.addWidget(QLabel(self.filename), 0, 1)

        self.gridlayout.addWidget(QLabel('Author:'), 1, 0)

        self.gridlayout.addWidget(QLabel('Review:'), 2, 0)

    def loadbagfile(self):
        # print("loadbagfile")
        self.filename = QFileDialog.getOpenFileName()
        print(self.filename)