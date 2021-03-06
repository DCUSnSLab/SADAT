import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from dadatype.dtype_cate import DataGroup
from taskLoopPlay import playbackInfo, taskLoopPlay


class taskPostPlan(QThread):
    infosignal = pyqtSignal([playbackInfo])
    signal = pyqtSignal([dict])
    imageSignal = pyqtSignal([dict])
    working = True

    def __init__(self, parent=None, simlog=None, extModule=None):
        super(taskPostPlan, self).__init__(parent=parent)
        self.extModMngr = extModule
        self.simlog = simlog

    def stop(self):
        self.working = False

    def run(self):
        lq = self.simlog.getQueuePlayData()
        pinfo = playbackInfo()
        pinfo.mode = taskLoopPlay.PLAYMODE_ETC
        for rawdata in iter(lq.get, 'interrupt'):
            dset = dict()
            imageset = dict()
            pinfo.lidartimestamp = ''
            ltime = 0
            imtime = 0
            self.extModMngr.doTask(rawdata)
            for dskey, dsv in self.extModMngr.getDataset().items():
                dset[dskey] = dsv

            for rwkey, val in self.extModMngr.getRawData().items():
                if val.dataGroup != DataGroup.GRP_DISPLAY:
                    dset[rwkey] = val
                    pinfo.lidartimestamp += "%.3f"%(dset[rwkey].getTimeStamp()) + ', '
                    ltime = dset[rwkey].getTimeStamp()
                else:
                    imageset[rwkey] = val
                    pinfo.lidartimestamp += "%.3f"%(imageset[rwkey].timestamp) + ', '
                    imtime = imageset[rwkey].timestamp

            gap = ltime - imtime
            pinfo.lidartimestamp += "%.3f"%(gap)
            #send all data to show in planview
            self.signal.emit(dset)
            self.imageSignal.emit(imageset)
            self.infosignal.emit(pinfo)
