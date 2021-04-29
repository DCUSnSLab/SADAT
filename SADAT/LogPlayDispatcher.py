import math
import json
import time
from PyQt5.QtCore import pyqtSignal

from Dispatcher import Dispatcher
from sensor.SenAdptMgr import AttachedSensorName
from utils.sadatlogger import slog


class LogPlayDispatcher(Dispatcher):

    def __init__(self, log, srcmgr):
        super().__init__()
        self.Log = log
        self.sourcemanager = srcmgr
        slog.DEBUG("-----LogPlayDispatcher Init-----")
        print(self.guiApp)

        self.testrawdata = []

    def dispatch(self):
        time.sleep(1)
        self.logDispatch()


    def logDispatch(self):
        logcnt = 0
        hasStartFlag = False

        tempX = []
        tempY = []
        tempXY = []
        timestamp = 0
        scan_cnt = 0

        logplaydata = self.Log.getQueueLoggingData()
        prevt = 0
        total = 0
        cnt = 0
        for dataset in iter(logplaydata.get, 'interrupt'):
            for key in dataset.keys():
                data = dataset[key]
                if key in self.sourcemanager.AllSensors.keys():
                    sensor = self.sourcemanager.AllSensors[key]
                    sensor.doWork(data)



                #tempdata = str(scan_cnt)+','+str(data['start_flag'])+','+str(data['angle'])+','+str(data['distance'])
                #self.testrawdata.append(tempdata)

        # for test
        # with open('../../LogPlayDisrawdata.json', 'w') as outfile:
        #     print('Raw data writing')
        #     #json.dump(self.testrawdata, outfile)
        #     for d in self.testrawdata:
        #         outfile.write(d+'\n')
        #     print("Raw data Write Complete")
        #self.Log.enQueueData(self.getEOFMessage())

# if __name__ == '__main__':
#     manager = Manager()
#     simlog = SimLog(manager)
#     gm = LogSimDispatcher(simlog)
#     gm.dispatch()