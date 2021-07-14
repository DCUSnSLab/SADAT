import math
import json
import time
from PyQt5.QtCore import pyqtSignal

from grabber.Dispatcher import Dispatcher
from sensor.SenAdptMgr import AttachedSensorName
from utils.sadatlogger import slog


class LogPlayDispatcher(Dispatcher):

    def __init__(self, srcmgr):
        super().__init__()
        self.sourcemanager = srcmgr
        slog.DEBUG("-----LogPlayDispatcher Init-----")
        print(self.guiApp)

    def dispatch(self):
        time.sleep(1)
        self.logDispatch()

    def logDispatch(self, logplaydata):
        for key in logplaydata.keys():
            data = logplaydata[key]
            if key in self.sourcemanager.AllSensors.keys():
                sensor = self.sourcemanager.AllSensors[key]
                sensor.doWork(data)