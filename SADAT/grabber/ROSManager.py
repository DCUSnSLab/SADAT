from time import sleep

from grabber.GrabberROS import GrabberROS
from utils.importer import Importer
from utils.sadatlogger import slog
from sensor.SenAdptMgr import AttachedSensorName

class ROSManager:
    def __init__(self, srcmanager):
        self.topic_lists = dict()
        self.enabledTopics = list()
        self.srcmanager = srcmanager

        try:
            self.rospy = Importer.importerLibrary('rospy')
        except:
            self.rospy = None

        self.enabledTopics.append(AttachedSensorName.USBCAM)
        self.enabledTopics.append(AttachedSensorName.ZEDCAM)
        #self.enabledTopics.append('/scan')
        self.enabledTopics.append(AttachedSensorName.VelodyneVLC16)

    def enableTopic(self, key):
        if key in self.enabledTopics is not True:
            self.enabledTopics.append(key)

    def disableTopic(self, key):
        try:
            self.enabledTopics.remove(key)
            return True
        except:
            return False

    def generateTopics(self, dispatcher):
        grablist = list()
        for et in self.enabledTopics:
            topicname = et.getTopicName()
            #print(topicname)
            #print(self.topic_lists)
            if topicname in self.topic_lists:
                sectopic = self.topic_lists[topicname]
                attchedsensor = et
                grabname = str(attchedsensor).split('.')[1] + 'grabber'
                #grablist.append([et, sectopic])
                grablist.append(GrabberROS(disp=dispatcher, senstype=[attchedsensor], nodename=grabname, topic=[topicname, sectopic]))
            else:
                emsg = 'no topic in available topic list - ' + str(et)
                slog.DEBUG(emsg)
        return grablist

    def getTopicLists(self):
        return self.topic_lists


    def refreshTopicList(self):
        try:
            if self.rospy == None:
                return

            slog.DEBUG('-----published topic lists-----')
            for data in self.rospy.get_published_topics():
                hassensor = False
                for enabledSensor in self.enabledTopics:
                    if data[0] == enabledSensor.getTopicName():
                        hassensor = True
                if hassensor:
                    slog.DEBUG(data)
                    msgs = data[1].split('/')
                    from_str = msgs[0] + '.msg'
                    import_str = msgs[1]
                    try:
                        msg = Importer.importerLibrary(from_str, import_str)
                        self.topic_lists[data[0]] = msg
                    except Exception as e:
                        db = 'Import error - No Modules as ' + str(e)
                        slog.DEBUG(db)
        except Exception as e:
            db = 'refresh error - '+str(e)
            slog.DEBUG(db)

        return self.topic_lists