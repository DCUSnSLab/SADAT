from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initialize()

    def initialize(self):
        self.setGeometry(300, 300, 400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("PyQt5 Ex!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont('Hack', 15))
        layout.addWidget(self.label)

        button = QPushButton("Press Button!")
        button.clicked.connect(self.button_clicked)
        button.setFont(QtGui.QFont('Hack', 15))
        layout.addWidget(button)

    def button_clicked(self):
        print("Button Clicked", self.count)
        # QMessageBox.about(self, "Alert", "Clicked!")
        self.count += 1
        self.label.setText("Count " + str(self.count))


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())