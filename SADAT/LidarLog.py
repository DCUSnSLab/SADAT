import json

from LogP import LogP

class LidarLog(LogP):
    motorpwm = 0

    def __init__(self, manager):
        super().__init__()

        self.lidarDataQueue = self.addQueueList(manager.Queue())
        # self.rawdata = [] #for test

    def initLog(self, motorpwm):
        self.motorpwm = motorpwm

        if not self.lidarDataQueue.empty():
            while not self.lidarDataQueue.empty():
                self.lidarDataQueue.get()

    def makeData(self, scandata, timestamp):
        data = {}
        data['start_flag'] = scandata.start_flag
        data['quality'] = scandata.quality
        data['angle'] = scandata.angle
        data['distance'] = scandata.distance
        data['timestamp'] = timestamp
        return data

    def makeDatafromROS(self, angle, range, cnt, timestamp):
        data = {}
        if cnt == 0:
            data['start_flag'] = True
        else:
            data['start_flag'] = False

        data['quality'] = None
        data['angle'] = angle
        data['distance'] = range
        data['timestamp'] = timestamp
        return data

    def enQueueDataNew(self, scandata):
        if scandata == 'interrupt':
            self.lidarDataQueue.put(scandata)
        else:
            self.lidarDataQueue.put(scandata)

    def enQueueData(self, scandata, timestamp):
        if scandata == 'interrupt':
            self.lidarDataQueue.put(scandata)

            # #for test
            # with open('../../rawdata.json','w') as outfile:
            #     print('Raw data writing')
            #     json.dump(self.rawdata, outfile)
            #     print("Raw data Write Complete")
        else:
            data = {}
            data['start_flag'] = scandata.start_flag
            data['quality'] = scandata.quality
            data['angle'] = scandata.angle
            data['distance'] = scandata.distance
            data['timestamp'] = timestamp
            #print(data['start_flag'],data['angle'], data['distance'])
            self.lidarDataQueue.put(data)

            # tempdata = str(data['start_flag'])+','+str(data['angle'])+','+str(data['distance'])
            # self.rawdata.append(tempdata)


    def getQueueData(self):
        return self.lidarDataQueue
