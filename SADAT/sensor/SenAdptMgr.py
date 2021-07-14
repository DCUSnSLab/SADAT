from enum import Enum
from sensor.psensor.RPLidar2D import RPLidar2DA3
from sensor.psensor.USBCAM import USBCAM
from sensor.psensor.Velodyne3D import Velodyne3D
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv
from sensor.vsensor.Track import Track

class AttachedSensorName(Enum):
    RPLidar2DA3 = '/scan'
    RPLidar2DVirtual = '/scanv'
    Tracker1 = '/track'
    USBCAM = '/usb_cam/image_raw/compressed'
    VelodyneVLC16 = '/velodyne_points'

class SenAdptMgr:
    def __init__(self, srcmanager, manager):
        self.srcmanager = srcmanager
        self.manager = manager
        self.__initDevices()

    def __initDevices(self):
        self.srcmanager.init()
        #actual Device
        self.__addActualSensor(RPLidar2DA3(AttachedSensorName.RPLidar2DA3))
        self.__addActualSensor(USBCAM(AttachedSensorName.USBCAM))
        self.__addActualSensor(Velodyne3D(AttachedSensorName.VelodyneVLC16))

        #virtual Device
        self.__addVirtualSensor(Track(AttachedSensorName.Tracker1))
        self.__addVirtualSensor(RPLidar2Dv(AttachedSensorName.RPLidar2DVirtual))

    def __addActualSensor(self, sensor):
        self.srcmanager.addActualSensor(sensor, self.manager)

    def __addVirtualSensor(self, sensor):
        self.srcmanager.addVirtualSensor(sensor, self.manager)