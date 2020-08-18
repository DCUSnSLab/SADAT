import time

class SimLog:

    def __init__(self, manager):
        print("Sim Log Init")
        self.simLogData = manager.Queue()
        self.playData = manager.Queue()

    def initLog(self):

        if not self.simLogData.empty():
            while not self.simLogData.empty():
                self.simLogData.get()

    def enQueueData(self, data):
        qsize = self.simLogData.qsize()
        # while qsize > 1000:
        #     time.sleep(0.001)
        #     qsize = self.simLogData.qsize()

        self.simLogData.put(data)

    def getQueueData(self):
        return self.simLogData

    def enQueuePlayData(self, data):
        self.playData.put(data)

    def getQueuePlayData(self):
        return self.playData

