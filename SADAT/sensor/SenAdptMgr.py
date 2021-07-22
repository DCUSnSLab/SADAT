from enum import Enum
from sensor.psensor.RPLidar2D import RPLidar2DA3
from sensor.psensor.USBCAM import USBCAM
from sensor.psensor.Velodyne3D import Velodyne3D
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv
from sensor.vsensor.Track import Track

class AttachedSensorName(Enum):
    RPLidar2DA3 = 'rplidar:/scan:/scan'
    RPLidar2DVirtual = 'rplidarVR:/scanv:/scanv'
    Tracker1 = 'track:/track:/track'
    USBCAM = 'usbcam:/usb_cam/image_raw/compressed:sensor_msgs/CompressedImage'
    ZEDCAM = 'zedcam:/zed2/zed_node/right/image_rect_color/compressed:sensor_msgs/CompressedImage'
    VelodyneVLC16 = 'velodyne:/velodyne_points:pointcloud2'

    def getTopicName(inst):
        tname = inst.value.split(':')[1]
        return tname

class SenAdptMgr:
    def __init__(self, srcmanager, manager, sysmanager):
        self.srcmanager = srcmanager
        self.manager = manager
        self.sysmanager = sysmanager
        self.__initDevices()

    def __initDevices(self):
        self.srcmanager.init()
        #actual Device
        self.__addActualSensor(USBCAM(AttachedSensorName.USBCAM))
        self.__addActualSensor(USBCAM(AttachedSensorName.ZEDCAM))
        self.__addActualSensor(RPLidar2DA3(AttachedSensorName.RPLidar2DA3))
        self.__addActualSensor(Velodyne3D(AttachedSensorName.VelodyneVLC16, self.sysmanager.psignal))

        #virtual Device
        self.__addVirtualSensor(Track(AttachedSensorName.Tracker1))
        self.__addVirtualSensor(RPLidar2Dv(AttachedSensorName.RPLidar2DVirtual))

    def __addActualSensor(self, sensor):
        self.srcmanager.addActualSensor(sensor, self.manager)

    def __addVirtualSensor(self, sensor):
        self.srcmanager.addVirtualSensor(sensor, self.manager)