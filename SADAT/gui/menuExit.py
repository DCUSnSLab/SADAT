from PyQt5.QtWidgets import qApp, QAction

class menuExit(QAction):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.prt = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')

    def trig(self):
        self.prt.simulator.cleanProcess()
        qApp.quit()
