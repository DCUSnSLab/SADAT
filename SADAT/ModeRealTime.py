from Grabber import Grabber
from GrabberROS import GrabberROS
from GrabberROSCam import GrabberROSCam
from GrabberROSSync import GrabberROSSync
from GrabberROSVelodyne import GrabberROSVelodyne
from GrabberROSrplidar import GrabberROSrplidar
from LogPlayDispatcher import LogPlayDispatcher
from Logger import Logger
from simMode import Mode


class ModeRealTime(Mode):
    def __init__(self, log, simlog, srcmgr):
        super().__init__(log)
        #init grabber
        self.grabber = None
        self.logger = Logger(self.log, simlog)
        self.dispatcher = LogPlayDispatcher(srcmgr)

    def makeProcess(self):
        print("MakeProcess : Log Type :",self.currentMode)
        if self.currentMode is self.LOGTYPE_DEVICE:
            self.grabber = Grabber(self.log, 1000)
            self.addProcess("Grabber", self.grabber.startGrab, None)
        else:
            self.grabber = GrabberROSrplidar(self.dispatcher)
            self.camgrabber = GrabberROSCam(self.dispatcher)
            self.velograbber = GrabberROSVelodyne(self.dispatcher)
            #self.syncgrabber = GrabberROSSync(self.dispatcher)
            self.addProcess("ROS Grabber RPlidar", self.grabber.startGrab, None)
            self.addProcess("ROS Grabber Cam", self.camgrabber.startGrab, None)
            self.addProcess("ROS Velodyne Lidar", self.velograbber.startGrab, None)
            #self.addProcess("ROS Grabber Sync", self.syncgrabber.startGrab, None)

        self.addProcess("Logger", self.logger.LogWorker, None)
        #self.addProcess("LogDispatcher", self.dispatcher.dispatch, None)