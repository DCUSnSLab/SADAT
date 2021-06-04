from abc import *
from SimProcess import SimProcess


class Mode(metaclass=ABCMeta):
    MODE_LOG = 1
    MODE_SIM = 2

    LOGTYPE_DEVICE = 1
    LOGTYPE_ROS = 2

    def __init__(self, log):
        self.log = log
        self.procList = []
        self.lSimDispatcher = None
        self.currentMode = self.LOGTYPE_DEVICE

    def addProcess(self, name, func, args):
        self.procList.append(SimProcess(name=name, target=func, args=args))

    def getProcesses(self):
        self.procList.clear()

        if len(self.procList) == 0:
            self.makeProcess()
        return self.procList

    def getHandledProcesses(self):
        return self.procList

    def setVelocity(self, vel):
        if self.lSimDispatcher is not None:
            self.lSimDispatcher.setVelocity(vel)

    def setLogType(self, type):
        print("set Log Mode",type)
        self.currentMode = type

    @abstractmethod
    def makeProcess(self):
        pass
