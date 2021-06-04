from abc import *
import datetime as pydatetime
from multiprocessing import Value
from utils.importer import Importer


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()

class GrabberROS(metaclass=ABCMeta):
    def __init__(self, disp: 'LogPlayDispatcher', senstype=list(), nodename=None, topicname=None):
        self._node = nodename
        self._senstype = senstype
        self._rosTopic = dict()
        self._dispatcher = disp
        self._initpass = True
        self.Signal = Value('i', 0)

        self._msgtype = list()

        #init ros library
        self.rospy = None
        self.message_filters = None

        print(topicname)
        if topicname != None:
            if isinstance(topicname, list) is True:
                for tn in topicname:
                    self._rosTopic['/'+tn] = None
            else:
                self._rosTopic['/'+topicname] = None

            self._initMsgType()
        else:
            self._initpass = False

    def _initMsgType(self):
        print('init msgtype')
        try:
            checkinit = True
            # Import LaserScan
            self.rospy = Importer.importerLibrary('rospy')
            self.message_filters = Importer.importerLibrary('message_filters')

            for tn in self._rosTopic.keys():
                self._rosTopic[tn] = self.__getMsgType(tn)
            print(self._rosTopic)
            if checkinit is True:
                self._initpass = True
            else:
                self._initpass = False
        except Exception as e:
            print("Exception",e)
            self._initpass = False

    def __getMsgType(self, topicname):
        msgt = None
        if topicname == '/scan':
            print('set msgtype')
            msgt = Importer.importerLibrary('sensor_msgs.msg', 'LaserScan')
        elif topicname == '/usb_cam/image_raw/compressed':
            msgt = Importer.importerLibrary('sensor_msgs.msg', 'CompressedImage')
        elif topicname == '/usb_cam/image_raw':
            msgt = Importer.importerLibrary('sensor_msgs.msg', 'Image')
        elif topicname == '/velodyne_points':
            msgt = Importer.importerLibrary('sensor_msgs.msg', 'PointCloud2')
        else:
            msgt = None

        return msgt

    def connect(self):
        pass

    def startGrab(self):
        print('start grab')
        if self._initpass is True:
            self.connect()
            self.doGrab()
            self.disconnect()
        else:
            print('Grab Stopped due to init Failed -',self._node)

    def doGrab(self):
        print('init ROS Node -',self._node)
        self.rospy.init_node(self._node)
        sub = list()
        if len(self._senstype) == 1:
            for key, value in self._rosTopic.items():
                sub.append(self.rospy.Subscriber(key, value, self.callback))
        else:
            for key, value in self._rosTopic.items():
                sub.append(self.message_filters.Subscriber(key, value))

            ts = self.message_filters.ApproximateTimeSynchronizer(sub, 10, 0.1, allow_headerless=True)
            ts.registerCallback(self.callback)
        self.rospy.spin()

    def callback(self, *msgs):
        if self.Signal.value == 1:
            print("Set Signal 1")
            self.disconnectSignal()
        else:
            self.userCallBack(msgs)

    def sendData(self, data, senstype: 'AttachedSensorName'=None):
        if senstype is None:
            senstype = self._senstype[0]

        senddata = {senstype: data}
        self._dispatcher.logDispatch(senddata)

    @abstractmethod
    def userCallBack(self, msgs):
        pass

    def disconnect(self):
        print("ROS Grappber disconnect", self._node)
        self.Signal.value = 1
        #self.rospy.signal_shutdown("reason")
        #self.rospy.on_shutdown(self.callback)
        #print('ROS Disconnected 1')

    def disconnectSignal(self):
        print('ROS Disconnected 2')
        self.rospy.signal_shutdown("reason")
        print('ROS Disconnected 3')
