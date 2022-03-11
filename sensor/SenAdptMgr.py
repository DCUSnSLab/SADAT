from enum import Enum
from sensor.psensor.RPLidar2D import RPLidar2DA3
from sensor.psensor.SPFloat import SPFloat
from sensor.psensor.USBCAM import USBCAM
from sensor.psensor.Velodyne3D import Velodyne3D
from sensor.psensor.ZedTrack import ZedTrack
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv
from sensor.psensor.Track import Track

#class ROSmsgType(Enum):
from utils.sadatlogger import slog


class AttachedSensorName(Enum):
    #Physical
    RPLidar2DA3 = 'rplidar:/scan:/scan'
    LidarTracker = 'lidartrack:/lidar_tracker_geometry:geometry_msgs/PoseArray'
    CamTracker = 'camtrack:/cam_tracker_geometry:geometry_msgs/PoseArray'
    ZED_ObjectDet = 'zedobjdet:/zed2/zed_node/obj_det/objects:zed_interfaces/ObjectsStamped'
    USBCAM = 'usbcam:/usb_cam/image_raw/compressed:sensor_msgs/CompressedImage'
    ZEDCAM = 'zedcam:/zed2/zed_node/left/image_rect_color/compressed:sensor_msgs/CompressedImage'
    VelodyneVLC16 = 'velodyne pointcloud:/velodyne_points:pointcloud2'
    CarlaLidar = 'carlaLidar:/carla/ego_vehicle/lidar:pointcloud2'
    KittiLidar = 'kittiLidar:/kitti/velo/pointcloud:pointcloud2'
    SPFloat = 'speedfloat:/vesc/commands/motor/speed:std_msg/Float64'
    #Virtual
    RPLidar2DVirtual = 'rplidarVR:/scanv:/scanv'

    def getInstance(inst):
        if inst.getMsgType() == 'scan':
            return RPLidar2DA3(inst)
        elif inst.getMsgType() == 'geometry_msgs/PoseArray':
            return Track(inst)
        elif inst.getMsgType() == 'zed_interfaces/ObjectsStamped':
            return ZedTrack(inst)
        elif inst.getMsgType() == 'sensor_msgs/CompressedImage':
            return USBCAM(inst)
        elif inst.getMsgType() == 'pointcloud2':
            return Velodyne3D(inst)
        elif inst.getMsgType() == 'std_msg/Float64':
            return SPFloat(inst)

    def getTopicName(inst):
        tname = inst.value.split(':')[1]
        return tname

    def getName(inst):
        tname = inst.value.split(':')[0]
        return tname

    def getMsgType(inst):
        tname = inst.value.split(':')[2]
        return tname

class SensorItem:
    def __init__(self, sname):
        self.sensor = sname
        self.sensorName = sname.getName()
        self.msgType = sname.getMsgType()
        self.topicName = sname.getTopicName()

class SenAdptMgr:
    def __init__(self, srcmanager, manager, sysmanager):
        self.srcmanager = srcmanager
        self.manager = manager
        self.sysmanager = sysmanager
        self.sensorList = dict()
        self.__initDevices()

    def __initDevices(self):
        self.srcmanager.init()

        self.__makeSensorList()

        #actual Device
        # self.__addActualSensor(USBCAM(AttachedSensorName.USBCAM))
        # self.__addActualSensor(USBCAM(AttachedSensorName.ZEDCAM))
        # self.__addActualSensor(RPLidar2DA3(AttachedSensorName.RPLidar2DA3))
        # self.__addActualSensor(Velodyne3D(AttachedSensorName.VelodyneVLC16))

        #virtual Device
        #self.__addVirtualSensor(Track(AttachedSensorName.Tracker))
        self.__addVirtualSensor(RPLidar2Dv(AttachedSensorName.RPLidar2DVirtual))

    def __makeSensorList(self):
        for key, value in AttachedSensorName.__dict__['_value2member_map_'].items():
            sitem = SensorItem(value)
            self.sensorList[sitem.topicName] = sitem

    def addActualSensor(self, topic):
        sensoritem = self.sensorList[topic]
        nsensor = AttachedSensorName.getInstance(sensoritem.sensor)
        print(sensoritem.sensor, nsensor)
        self.__addActualSensor(nsensor)

    def __addActualSensor(self, sensor):
        self.srcmanager.addActualSensor(sensor, self.manager)

    def __addVirtualSensor(self, sensor):
        self.srcmanager.addVirtualSensor(sensor, self.manager)

    def getRegisteredSensors(self):
        return self.sensorList

    def getRegisteredSensorbyTopic(self, topic):
        if topic in self.sensorList.keys():
            return self.sensorList[topic]
        else:
            return None