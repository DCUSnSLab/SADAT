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
        self.GrabberTimeGap = 0.5
        try:
            self.rospy = Importer.importerLibrary('rospy')
            self.rosgraph = Importer.importerLibrary('rosgraph')
        except:
            self.rospy = None
            self.rosgraph = None

        # self.enabledTopics.append(AttachedSensorName.USBCAM)
        # self.enabledTopics.append(AttachedSensorName.ZEDCAM)
        # #self.enabledTopics.append('/scan')
        # self.enabledTopics.append(AttachedSensorName.VelodyneVLC16)

    def isWorkROS(self):
        if self.rospy is None:
            return False
        else:
            return True

    def enableTopic(self, key):
        if key in self.enabledTopics:
            slog.WARNING('aready in enabledTopis - '+str(key))
        else:
            self.enabledTopics.append(key)
            slog.DEBUG('registered enabled topic list in ROSManager %s' % str(key.getTopicName()))



    def disableTopic(self, key):
        try:
            self.enabledTopics.remove(key)
            return True
        except:
            return False

    def generateTopics(self, dispatcher):
        grablist = list()
        timecounter = 0.0
        for et in self.enabledTopics:
            topicname = et.getTopicName()
            #print(topicname)
            #print(self.topic_lists)
            if topicname in self.topic_lists:
                sectopic = self.topic_lists[topicname]
                attchedsensor = et
                grabname = str(attchedsensor).split('.')[1] + 'grabber'
                #grablist.append([et, sectopic])
                grablist.append(GrabberROS(disp=dispatcher, senstype=[attchedsensor], nodename=grabname, topic=[topicname, sectopic], counter=timecounter))
                timecounter += self.GrabberTimeGap
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

    def refreshAllTopicList(self):
        atopiclist = dict()
        try:
            if self.rospy == None:
                return

            slog.DEBUG('-----published topic lists-----')
            for data in self.rospy.get_published_topics():
                slog.DEBUG(data)
                msgs = data[1].split('/')
                from_str = msgs[0] + '.msg'
                import_str = msgs[1]
                try:
                    msg = Importer.importerLibrary(from_str, import_str)
                    atopiclist[data[0]] = msg
                except Exception as e:
                    db = 'Import error - No Modules as ' + str(e)
                    slog.DEBUG(db)
        except Exception as e:
            db = 'refresh error - '+str(e)
            slog.DEBUG(db)

        return atopiclist

    def isROSMasterWorking(self):
        try:
            return 'True, pid: ' + str(self.rosgraph.Master('/rostopic').getPid())
        except Exception:
            print('ros master')
            return False