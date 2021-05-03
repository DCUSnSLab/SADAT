from externalmodules.extModule import extModule

class trackerBasic(extModule):
    def __init__(self):
        super().__init__('trackerBasic')
        #self.tracker = mytracker.Tracker(100, 2)

    def getRawDatabyKey(self, key):
        return self._getRawDatabyKey(key)

    def getLidarDatabyKey(self, key):
        return self._getData()

    def do(self):
        pass
