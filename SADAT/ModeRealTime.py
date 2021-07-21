from time import sleep

from grabber.Grabber import Grabber
from grabber.LogPlayDispatcher import LogPlayDispatcher
from Logger import Logger
from simMode import Mode
from utils.sadatlogger import slog


class ModeRealTime(Mode):
    def __init__(self, log, simlog, srcmgr, rosmgr):
        super().__init__(log)
        #init grabber
        self.grabber = None
        self.logger = Logger(self.log, simlog)
        self.dispatcher = LogPlayDispatcher(srcmgr)
        self.rosmanager = rosmgr

    def makeProcess(self):
        slog.DEBUG("MakeProcess : Log Type :"+str(self.currentMode))
        if self.currentMode is self.LOGTYPE_DEVICE:
            self.grabber = Grabber(self.log, 1000)
            self.addProcess("Grabber", self.grabber.startGrab, None)
        else:
            self.rosmanager.refreshTopicList()
            topics = self.rosmanager.generateTopics(self.dispatcher)

            for grab in topics:
                self.addProcess(grab._node, grab.startGrab, None)


        #self.addProcess("Logger", self.logger.LogWorker, None)
        #self.addProcess("LogDispatcher", self.dispatcher.dispatch, None)