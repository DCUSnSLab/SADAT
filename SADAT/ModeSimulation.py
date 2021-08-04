from grabber.LogSimDispatcher import LogSimDispatcher
from simMode import Mode


class ModeSimulation(Mode):
    def __init__(self, srcmgr):
        super().__init__(None)
        self.lSimDispatcher = LogSimDispatcher(srcmgr)

    def makeProcess(self):
        self.addProcess("FileReader", self.lSimDispatcher.dispatch, None)