from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

# creating checkable combo box class
class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))

        # when any item get pressed

    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)

        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

            # calling method
        self.check_items()

        # method called by check_items

    def item_checked(self, index):

        # getting item at index
        item = self.model().item(index, 0)

        # return true if checked else false
        return item.checkState() == Qt.Checked

        # calling method

    def check_items(self):
        # blank list
        self.checkedItems = []

        # traversing the items
        for i in range(self.count()):

            # if item is checked add it to the list
            if self.item_checked(i):
                self.checkedItems.append(i)
                #print(i) 여기서 값을 받아옴
