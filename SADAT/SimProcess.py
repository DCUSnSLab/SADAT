class SimProcess:
    name = ""
    target = None
    args = None
    def __init__(self, name, target, args):
        self.name = name
        self.target = target
        self.args = args
        self.pid = None

    def setProcess(self, p):
        self.pid = p

    def getProcess(self):
        return self.pid

    def terminate(self):
        print('proc-',self.name,'terminated')
        self.pid.terminate()

    def is_alive(self):
        return self.pid.is_alive()