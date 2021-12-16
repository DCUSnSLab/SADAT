from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class vehicleInfoTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAlternatingRowColors(True)
        self.header().setVisible(False)

        itemTop1 = QTreeWidgetItem(self)
        itemTop1.setText(0, "Test1")
        itemChild1 = QTreeWidgetItem(itemTop1)
        itemChild1.setText(0, "ChildTest1")
        itemChild2 = QTreeWidgetItem(itemTop1)
        itemChild2.setText(0, "ChildTest2")
        itemTop1 = QTreeWidgetItem(self)
        itemTop1.setText(0, "Test2")