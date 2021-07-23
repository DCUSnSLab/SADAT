import logging
import sys
from time import sleep

from PyQt5 import QtGui
from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QFileDialog, QWidget, QDialog, QPlainTextEdit, QHBoxLayout, \
    QVBoxLayout, QGridLayout, QPushButton, QListView
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from simMode import Mode
from utils.sadatlogger import slog

class LogStringHandler(logging.Handler):
    def __init__(self, target_widget):
        super(LogStringHandler, self).__init__()
        self.target_widget = target_widget

    def emit(self, record):
        self.target_widget.appendPlainText(record.asctime + '-' + record.levelname + ' - ' + record.getMessage())
        cursor = self.target_widget.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.target_widget.setTextCursor(cursor)

class guiROSManager(QDialog):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.simulator = self.parent.simulator
        self.rosmanager = self.simulator.rosManager
        self.senadapter = self.simulator.senadapter
        self.srcmanager = self.simulator.srcmanager

        #LatesttopicList
        self.latestTopics = None
        #stream
        self.statuseditor = QPlainTextEdit(self)
        self.logstream = LogStringHandler(self.statuseditor)

        self.setWindowTitle('ROS Open Manager')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(1000, 700)

        #set dialog location center of parent
        qr = self.parent.frameGeometry()
        nr = self.frameGeometry()
        x = qr.left() + (qr.width() / 2 - nr.width() / 2)
        y = qr.top() + (qr.height() / 2 - nr.height() / 2)
        self.move(x, y)

        self.initUI()

        self.show()

        self.rosChecker()
        self.initTopics()


    def initUI(self):

        self.text1 = QPlainTextEdit('Published Topics')
        self.text1.setMaximumHeight(30)
        self.text2 = QPlainTextEdit('Topics for Grab')
        self.text2.setMaximumHeight(30)
        self.titlebox = QHBoxLayout()
        self.titlebox.addWidget(self.text1)
        self.titlebox.addWidget(self.text2)


        #ListBox
        self.listview1 = QListView(self)
        self.rosTopicModel = QStandardItemModel()
        self.listview1.setModel(self.rosTopicModel)
        self.listview1.clicked.connect(self.rosTopicListCheked)
        self.listview2 = QListView(self)
        self.actuateModel = QStandardItemModel()
        self.listview2.setModel(self.actuateModel)

        self.listbox = QHBoxLayout()
        self.listbox.addWidget(self.listview1)
        self.listbox.addWidget(self.listview2)


        #Button
        self.btnClear = QPushButton("ClearTopics")
        self.btnClear.clicked.connect(self.btnClearClicked)
        self.btnOK = QPushButton("Run")
        self.btnOK.clicked.connect(self.btnOKClicked)
        self.btnRunAllAvailable = QPushButton("Run All Available Topics")
        self.btnRunAllAvailable.clicked.connect(self.btnAllClicked)
        self.buttonbox = QHBoxLayout()
        self.buttonbox.addWidget(self.btnClear)
        self.buttonbox.addWidget(self.btnOK)
        self.buttonbox.addWidget(self.btnRunAllAvailable)


        self.statuseditor.setMaximumHeight(150)
        self.statuseditor.document().setDocumentMargin(0)
        self.statuseditor.horizontalScrollBar().setVisible(False)
        self.statuseditor.horizontalScrollBar().setDisabled(True)
        self.statusbox = QHBoxLayout()
        self.statusbox.addWidget(self.statuseditor)


        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.titlebox)
        self.mainlayout.addLayout(self.listbox)
        self.mainlayout.addLayout(self.buttonbox)
        self.mainlayout.addLayout(self.statusbox)
        self.setLayout(self.mainlayout)

        slog.addHandler(self.logstream)
        #self.layout().addWidget(self.editor)

    def rosChecker(self):
        slog.DEBUG('rospy status check : '+str(self.rosmanager.isWorkROS()))
        slog.DEBUG('ros master status check : ' + str(self.rosmanager.isROSMasterWorking()))

    def initTopics(self):
        self.cleanViewModel(self.rosTopicModel)
        self.cleanViewModel(self.actuateModel)
        self.refreshTopics(self.rosTopicModel)


    def refreshTopics(self, listmodel):
        self.latestTopics = self.rosmanager.refreshAllTopicList()
        for key, value in self.latestTopics.items():
            kitem = key
            nitem = QStandardItem()
            if self.isAvailableSensor(key):
                kitem = str(kitem) + ' [A]'
                nitem.setText(kitem)
                qf = nitem.font()
                qf.setBold(True)
                nitem.setFont(qf)
                nitem.setForeground(Qt.red)

            else:
                nitem.setText(kitem)
            listmodel.appendRow(nitem)

    def appendListViewItems(self, viewmodel, item):
        viewmodel.appendRow(QStandardItem(item))

    def cleanViewModel(self, viewmodel):
        viewmodel.clear()

    def getValuefromListViewItem(self, item):
        items = str(item).split(' ')
        if len(items) > 1:
            return items[0]
        else:
            return item

    def moveAvailableTopics(self):
        movedindex = list()
        for idx in range(self.rosTopicModel.rowCount()):
            #get data from actuate
            index = self.rosTopicModel.index(idx,0)
            item = self.rosTopicModel.itemData(index)
            topic = item[0]
            gitem = self.getValuefromListViewItem(topic)
            if self.isAvailableSensor(gitem):
                self.appendListViewItems(self.actuateModel, gitem)
                movedindex.append(index)

        accidx = 0
        for idx in movedindex:
            self.rosTopicModel.removeRow(idx.row() - accidx)
            accidx += 1

    def isAvailableSensor(self, key):
        if self.senadapter.getRegisteredSensorbyTopic(key) is not None:
            slog.DEBUG('Available Topic - ' + key + '- True')
            return True
        else:
            return False

    def submitSensor(self):
        ischecked = False

        for idx in range(self.actuateModel.rowCount()):
            #get data from actuate
            index = self.actuateModel.index(idx,0)
            item = self.actuateModel.itemData(index)
            topic = item[0]
            #add Actual Sensor using ros Topic
            self.senadapter.addActualSensor(topic)

            #enable ROS topic in ROS Manager
            self.rosmanager.enableTopic(self.senadapter.getRegisteredSensorbyTopic(topic).sensor)
            ischecked = True

        return ischecked

    def runROS(self):
        self.parent.simulator.setAction(Mode.MODE_LOG, Mode.LOGTYPE_ROS)
        self.parent.simulator.playMode()

    #events
    def btnClearClicked(self, event):
        self.initTopics()

    def btnOKClicked(self, event):
        if self.submitSensor() is True:
            self.runROS()
            self.close()


    def btnAllClicked(self, event):
        self.moveAvailableTopics()

        if self.submitSensor() is True:
            self.runROS()
            #self.close()


    def rosTopicListCheked(self, index):
        item = self.rosTopicModel.itemData(index)
        for key, value in item.items():
            gitem = self.getValuefromListViewItem(value)
            if self.isAvailableSensor(gitem):
                self.appendListViewItems(self.actuateModel, gitem)
                self.rosTopicModel.removeRow(index.row())
            else:
                slog.DEBUG('Unavailable Topic - '+gitem+' not registered in SADAT')

    def closeEvent(self, event):
        slog.DEBUG('close guiROSManager')
        slog.removeHandler(self.logstream)