import sys
from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.toolbar = QtWidgets.QToolBar("Example")
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)

        self.toolbar.addAction("action 1")
        self.toolbar.addAction("action 2")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())