import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        mainlayout = QVBoxLayout()

        button_1 = QPushButton("Test btn 1")
        button_2 = QPushButton("Test btn 2")
        button_3 = QPushButton("Test btn 3")
        button_4 = QPushButton("Test btn 4")
        button_5 = QPushButton("Test btn 5")
        button_6 = QPushButton("Test btn 6")
        button_7 = QPushButton("Test btn 7")

        ctrlayout = QHBoxLayout()
        algotestlayout = QVBoxLayout()
        algotestlayout.addWidget(button_1)
        algotestlayout.addWidget(button_2)

        replaylayout = QVBoxLayout()
        replaylayout.addWidget(button_3)
        replaylayout.addWidget(button_4)

        ctrlayout.addLayout(algotestlayout)
        ctrlayout.addLayout(replaylayout)

        mainlayout.addLayout(ctrlayout)

        playbacklayout = QHBoxLayout()

        playbacklayout.addWidget(button_5)
        playbacklayout.addWidget(button_6)
        playbacklayout.addWidget(button_7)

        mainlayout.addLayout(playbacklayout)

        self.setLayout(mainlayout)
        self.resize(500, 500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())