from grabber.Grabber import Grabber
from grabber.GrabberROSCam import GrabberROSCam
from grabber.GrabberROSVelodyne import GrabberROSVelodyne
from grabber.GrabberROSrplidar import GrabberROSrplidar
from grabber.LogPlayDispatcher import LogPlayDispatcher
from Logger import Logger
from simMode import Mode


class ModeRealTime(Mode):
    def __init__(self, log, simlog, srcmgr, rosmgr):
        super().__init__(log)
        #init grabber
        self.grabber = None
        self.logger = Logger(self.log, simlog)
        self.dispatcher = LogPlayDispatcher(srcmgr)
        self.rosmanager = rosmgr

    def makeProcess(self):
        print("MakeProcess : Log Type :",self.currentMode)
        if self.currentMode is self.LOGTYPE_DEVICE:
            self.grabber = Grabber(self.log, 1000)
            self.addProcess("Grabber", self.grabber.startGrab, None)
        else:
            # self.grabber = GrabberROSrplidar(self.dispatcher)
            # self.camgrabber = GrabberROSCam(self.dispatcher)
            # self.velograbber = GrabberROSVelodyne(self.dispatcher)
            #self.syncgrabber = GrabberROSSync(self.dispatcher)

            # self.addProcess("ROS Grabber RPlidar", self.grabber.startGrab, None)
            # self.addProcess("ROS Grabber Cam", self.camgrabber.startGrab, None)
            # self.addProcess("ROS Velodyne Lidar", self.velograbber.startGrab, None)
            #self.addProcess("ROS Grabber Sync", self.syncgrabber.startGrab, None)
            self.rosmanager.refreshTopicList()
            topics = self.rosmanager.generateTopics(self.dispatcher)

            for grab in topics:
                self.addProcess(grab._node, grab.startGrab, None)

        self.addProcess("Logger", self.logger.LogWorker, None)
        #self.addProcess("LogDispatcher", self.dispatcher.dispatch, None)