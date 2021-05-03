from Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog
from sensor.SenAdptMgr import AttachedSensorName
from sensor.SourceManager import SourceManager
from utils.sadatlogger import slog


class LogSimDispatcher(Dispatcher):

    def __init__(self, srcmgr:SourceManager, opensrc=""):
        super().__init__()
        self.sourcemanager = srcmgr
        self.opensrc = opensrc
        slog.DEBUG("LogSimDispatcher Init")

    def dispatch(self):
        self.loadData()
        self.logDispatch()
        self.sendEvent()

    def loadData(self):
        slog.DEBUG("-----lodata method called-----")
        if self.opensrc == "":
            self.opensrc = "../../Data/data_1.dat"

        #파일을 저장할 때 head 부분에 디바이스 네임을 작성해줘야함
        #헤더파일의 디바이스 네임에 따라 rawdata에 저장될 수 있도록 변경해야함
        lidarlog = makeRPLidarLog(self.opensrc);
        self._rawdata[AttachedSensorName.RPLidar2DVirtual] = lidarlog.fromlogFile()

    def logDispatch(self):
        for scate in self._rawdata.keys():
            if scate in self.sourcemanager.AllSensors.keys():
                val = self._rawdata[scate]
                sensor = self.sourcemanager.AllSensors[scate]
                sensor.doWork(val)
        slog.DEBUG("Data Load Finished")

    def sendEvent(self):
        slog.DEBUG("send Event")
        loadedsens = list()
        # send event to taskLoopPlay to wake up sim receive module
        for data in self._rawdata.keys():
            loadedsens.append(data)
        self.sourcemanager.simEvent(loadedsens)
