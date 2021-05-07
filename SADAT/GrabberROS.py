from abc import *
import datetime as pydatetime
from multiprocessing import Value
from utils.importer import Importer


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()

class GrabberROS(metaclass=ABCMeta):
    def __init__(self, disp: 'LogPlayDispatcher', senstype, nodename, topicname=None):
        self._node = nodename
        self._senstype = senstype
        self._dispatcher = disp
        self._initpass = True
        self.Signal = Value('i', 0)

        self._msgtype = None
        if topicname != None:
            self._topicName = '/'+topicname
            print(self._topicName)
            self._initMsgType()
        else:
            self._initpass = False

    def _initMsgType(self):
        print('init msgtype')
        try:
            checkinit = True
            # Import LaserScan
            self.rospy = Importer.importerLibrary('rospy')
            if self._topicName == '/scan':
                print('set msgtype')
                self._msgtype = Importer.importerLibrary('sensor_msgs.msg','LaserScan')
            elif self._topicName == '/usb_cam/image_raw/compressed':
                self._msgtype = Importer.importerLibrary('sensor_msgs.msg', 'CompressedImage')
            elif self._topicName == '/usb_cam/image_raw':
                self._msgtype = Importer.importerLibrary('sensor_msgs.msg', 'Image')
            else:
                self._msgtype = None
                checkinit = False

            if checkinit is True:
                self._initpass = True
            else:
                self._initpass = False
        except Exception as e:
            print("Exception",e)
            self._initpass = False

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
        sub = self.rospy.Subscriber(self._topicName, self._msgtype, self.callback)
        self.rospy.spin()

    def callback(self, msg):
        if self.Signal.value == 1:
            print("Set Signal 1")
            self.disconnectSignal()
        else:
            self.userCallBack(msg)

    def sendData(self, data):
        senddata = {self._senstype:data}
        self._dispatcher.logDispatch(senddata)

    @abstractmethod
    def userCallBack(self, msg):
        pass

    def disconnect(self):
        print("ROS Grappber disconnect", self._node)
        self.Signal.value = 1

    def disconnectSignal(self):
        self.rospy.signal_shutdown("reason")
        print('ROS Disconnected')
