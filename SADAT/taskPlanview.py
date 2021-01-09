import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class taskPlanview(QThread):
    signal = pyqtSignal([list])
    working = True

    def __init__(self, parent=None, simlog=None, extModule=None):
        super(taskPlanview, self).__init__(parent=parent)
        self.extModule = extModule
        self.simlog = simlog

    def stop(self):
        self.working = False

    def run(self):
        #pass
        lq = self.simlog.getQueuePlayData()
        for data in iter(lq.get, 'interrupt'):
            #data 형식을 바꿔야함 dtype_ 어쩌구로 바꿔줘야 함
            #전송되는 데이터의 형태도 다양해지기 때문에 dictionary 형태로 넘겨받아서 다시 extModule로 넘겨줘야 함
            self.extModule.doTask(data)
            #여기에 extAdapter를 통해서 외부 트래커 모듈을 동작
            self.signal.emit(data)
