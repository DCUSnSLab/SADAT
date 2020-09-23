from Grabber import Grabber
from GrabberROS import GrabberROS
from LogPlayDispatcher import LogPlayDispatcher
from Logger import Logger
from simMode import Mode


class ModeLog(Mode):
    def __init__(self, log, simlog):
        super().__init__(log)
        #init grabber
        self.grabber = None
        self.logger = Logger(self.log, simlog)
        self.dispatcher = LogPlayDispatcher(simlog)

    def makeProcess(self):
        print("MakeProcess : Log Type :",self.currentMode)
        if self.currentMode is self.LOGTYPE_DEVICE:
            self.grabber = Grabber(self.log, 1000)
            self.addProcess("Grabber", self.grabber.startGrab, None)
        else:
            self.grabber = GrabberROS(self.log)
            self.addProcess("ROS Grabber", self.grabber.startGrab, None)

        self.addProcess("Logger", self.logger.LogWorker, None)
        self.addProcess("LogDispatcher", self.dispatcher.dispatch, None)