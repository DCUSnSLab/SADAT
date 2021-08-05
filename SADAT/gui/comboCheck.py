from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

# creating checkable combo box class
class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self._changed = False
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel())

        # when any item get pressed

    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)
        data = item.data(Qt.UserRole)
        key = data[0]
        visibleobj = data[1]

        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            visibleobj[key] = False
        else:
            item.setCheckState(Qt.Checked)
            visibleobj[key] = True
        self._changed = True


    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def refreshList(self, objs):
        #print('triggered', objs)
        model = self.model()
        for key, boolean in objs.items():
            self.addItem(key.getName(), [key,objs])
        self.initchecker()

    def initchecker(self):
        for idx in range(self.count()):
            item = self.model().item(idx)
            if item.checkState() != QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Checked)
