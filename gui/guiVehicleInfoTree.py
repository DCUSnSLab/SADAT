from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class vehicleInfoTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.atree()

    def atree(self):
        self.setAlternatingRowColors(True)
        self.header().setVisible(True)
        self.setColumnWidth(0,250)
        self.headerItem().setText(0, "Display")
        self.headerItem().setText(1, " ")
        self.root = self.invisibleRootItem()

        itemTop1 = QTreeWidgetItem(self)
        itemTop1.setText(0, "Vehicle Info")
        itemChild1 = QTreeWidgetItem(itemTop1)
        itemChild1.setText(0, "IMU")
        itemChild1.setText(1, "0")
        itemChild2 = QTreeWidgetItem(itemTop1)
        itemChild2.setText(0, "vesc")
        itemChild3 = QTreeWidgetItem(itemChild2)
        itemChild3.setText(0, "commands")
        itemChild4 = QTreeWidgetItem(itemChild3)
        itemChild4.setText(0, "motor/speed")
        itemChild4.setText(1, "0")
        itemChild5 = QTreeWidgetItem(itemChild3)
        itemChild5.setText(0, "servo/positiom")
        itemChild5.setText(1, "0")
        itemChild6 = QTreeWidgetItem(itemChild3)
        itemChild6.setText(0, "odom")
        itemChild6.setText(1, "0")



        # self.setAlternatingRowColors(True)
        # self.header().setVisible(False)
        # self.tw = QTreeWidget(self)
        # self.tw.setColumnCount(2)
        # self.tw.setHeaderLabels(["Topic", "Data"])
        # self.root = self.tw.invisibleRootItem()
        #
        # item = QTreeWidgetItem()
        # item.setText(0, "Motor")
        # itemChild1 = QTreeWidgetItem(item)
        # itemChild1.setText(0, "speed")
        # itemChild1.setText(1, "0")
        # item2 = QTreeWidgetItem()
        # item2.setText(0, "Servo")
        # itemChild2 = QTreeWidgetItem(item2)
        # itemChild2.setText(0, "position")
        # itemChild2.setText(1, "0")
        #
        # self.root.addChild(item)
        # self.root.addChild(item2)
