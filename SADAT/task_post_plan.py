import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal



class taskPostPlan(QThread):
    signal = pyqtSignal([dict])
    working = True

    def __init__(self, parent=None, simlog=None, extModule=None):
        super(taskPostPlan, self).__init__(parent=parent)
        self.extModMngr = extModule
        self.simlog = simlog

    def stop(self):
        self.working = False

    def run(self):
        lq = self.simlog.getQueuePlayData()

        for rawdata in iter(lq.get, 'interrupt'):
            dset = dict()
            self.extModMngr.doTask(rawdata)
            for dskey, dsv in self.extModMngr.getDataset().items():
                dset[dskey] = dsv

            for rwkey, val in self.extModMngr.getRawData().items():
                dset[rwkey] = val


            #send all data to show in planview
            self.signal.emit(dset)
