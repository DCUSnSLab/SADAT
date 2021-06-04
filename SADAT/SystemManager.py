import sys
from multiprocessing import Manager, Process
from LidarLog import LidarLog
from ModeRealTime import ModeRealTime
from ModeSimulation import ModeSimulation
from SimLog import SimLog
from externalmodules.ext_module_manager import extModuleManager
from gui.guiMain import GUI_CONTROLLER
from sensor.SenAdptMgr import SenAdptMgr
from sensor.SourceManager import SourceManager
from simMode import Mode

from taskLoopPlay import taskLoopPlay
from task_post_plan import taskPostPlan
from utils.sadatlogger import slog


class SystemManager:
    processes = []

    def __init__(self, manager, gapp=None):
        self.guiApp = gapp
        self.manager = manager

        #sensor devices
        self.srcmanager = SourceManager(manager)
        self.senadapter = SenAdptMgr(self.srcmanager, manager)
        self.rawlog = LidarLog(manager)
        self.simlog = SimLog(manager)
        self.procs = {}
        self.pvthread = None
        self.lpthread = None

        #externalModules
        self.extModManager = extModuleManager()

        self.Velocity = 0

        self.plugins = None

        #for test
        self.srcmanager.printSensorList()
        self.loadPlugin()
        self.defineProcess()

        self.currentPlayMode = None

    def StartManager(self):
        # self.CommandMode()

        for p in self.processes:
            p.join()


    def setAction(self, mode, logtype=None):
        if mode is Mode.MODE_SIM:
            self.lpthread.setSimMode()
        elif mode is Mode.MODE_LOG:
            self.lpthread.setLoggingMode()
            #Need to modify for Logging during logplay
            #default simulation mode
            self.simlog.setLogPlayMode(SimLog.LOGPLAY_MODE_LOGPLAY)
            #self.simlog.setLogPlayMode(SimLog.LOGPLAY_MODE_SAVE)


        self.cleanProcess()
        proc = self.procs[mode]

        # set mode change
        self.currentPlayMode = mode

        #set Log Type
        if mode is Mode.MODE_LOG and logtype is not None:
            proc.setLogType(logtype)

        slog.DEBUG("Start Process")
        if proc is not None:
            # set Processes
            for pr in proc.getProcesses():
                self.addProcess(pr)
            for p in self.processes:
                p.start()
                #slog.DEBUG("Start"+p.name())

            # for data in iter(self.simlog.getQueueData().get, 'interrupt'):
            #     time.sleep(0.01)

    def cleanGrabber(self, procs=None):
        if self.currentPlayMode is Mode.MODE_LOG:
            #self.procs[Mode.MODE_LOG].grabber.Signal.value = 1
            for pr in self.procs[Mode.MODE_LOG].getHandledProcesses():
                if pr.is_alive():
                    pr.terminate()

            # self.procs[Mode.MODE_LOG].grabber.disconnect()
            # self.procs[Mode.MODE_LOG].camgrabber.disconnect()
            # self.procs[Mode.MODE_LOG].velograbber.disconnect()

            #print("print gcnt = ",self.procs[Mode.MODE_LOG].grabber.var1.value)

    def cleanProcess(self):
        slog.DEBUG('clean process')
        if len(self.processes) != 0:
            slog.DEBUG('clean grabber')
            self.cleanGrabber(self.processes)
            # clean process start

            # send interrupt message to logs
            # interrupt 를 enqueue했는데 더이상 빼가는 프로세스가 없으면 잔여 메세지가 남을 수 있고,
            # 추후 프로세스 새로 생성시 잔여 메시지 때문에 바로 프로세스가 멈출 가능성 있음
            self.rawlog.DisconnectLogs()
            self.simlog.DisconnectLogs()

            print("Wait process finishing for cleaning process list")
            for p in self.processes:
                p.join()

            self.processes.clear()
            print("Clean, process length :", len(self.processes))

    def defineProcess(self):
        # define system processes
        # init taskPostPlan thread
        # self.pvthread = taskPostPlan(self.guiApp, self.simlog, self.extModManager)
        # self.pvthread.signal.connect(self.guiApp.changePosition)
        # self.pvthread.imageSignal.connect(self.guiApp.updateCameraImage)
        # self.pvthread.infosignal.connect(self.guiApp.playbackstatus)
        # self.pvthread.start()

        self.lpthread = taskLoopPlay(self.guiApp, self.simlog, self.manager, self.srcmanager)
        self.lpthread.signal.connect(self.guiApp.playbackstatus)
        self.lpthread.dataSignal.connect(self.guiApp.changePosition)
        self.lpthread.imageSignal.connect(self.guiApp.updateCameraImage)
        self.lpthread.setVelocity(60)
        self.lpthread.start()

        # init log process
        self.procs[Mode.MODE_LOG] = ModeRealTime(self.rawlog, self.simlog, self.srcmanager)
        self.procs[Mode.MODE_SIM] = ModeSimulation(self.srcmanager)
        slog.DEBUG(self.procs)

    def addProcess(self, procdata):
        pr = None
        if procdata.args is None:
            pr = Process(name=procdata.name, target=procdata.target)
        else:
            pr = Process(name=procdata.name, target=procdata.target, args=procdata.args)
        procdata.setProcess(pr)
        self.processes.append(pr)


    def getNumofProc(self):
        return len(self.processes)

    def loadPlugin(self):
        self.plugins = []
        #self.plugins.append(Plugin())
        #플러그인 상속받은 Tracker Algorithm 생성

    def setVelocity(self, vel):
        v = int(vel)
        self.lpthread.setVelocity(v)
        self.Velocity = v

    def getVelocity(self):
        return self.Velocity

    def playMode(self):
        self.lpthread.setPlayMode()
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.PLAYMODE)

    def PauseMode(self):
        self.lpthread.setPause(False)
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.RESUMEMODE)

    def ResumeMode(self):
        self.lpthread.setPause(True)
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.PLAYMODE)


if __name__ == '__main__':
    gm = SystemManager(Manager())
    gm.StartManager()
