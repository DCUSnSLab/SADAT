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
            dataset = dict()
            dataset['rawdata'] = rawdata
            #data 형식을 바꿔야함 dtype_ 어쩌구로 바꿔줘야 함
            #전송되는 데이터의 형태도 다양해지기 때문에 dictionary 형태로 넘겨받아서 다시 extModule로 넘겨줘야 함
            self.extModMngr.doTask(rawdata)
            for dskey, dsv in self.extModMngr.getDataset().items():
                dataset[dskey] = dsv
            #send all data to show in planview
            self.signal.emit(dataset)
