from enum import Enum

from views.DataView import DataView
from views.viewLane import viewLane
from views.viewLine import viewLine
from views.viewpointcloud import viewPointCloud
from views.viewtrack import viewTrack


class DataGroup(Enum):
    GRP_POINTCLOUD = 1
    GRP_SINGLE_OBJECT = 2
    GRP_DISPLAY = 3
    GRP_ETC = 4


class DataTypeCategory(Enum):
    POINT_CLOUD = 1
    TRACK = 2
    LANE = 3
    LINE = 4
    TRAFFIC_SIGN = 5
    CAMERA = 11
    Float = 20
    Sensor = 21
    Odometry = 22

    def getInstance(inst):
        if inst == DataTypeCategory.POINT_CLOUD:
            return viewPointCloud()
        elif inst == DataTypeCategory.TRACK:
            return viewTrack()
        elif inst == DataTypeCategory.LANE:
            return viewLane()
        elif inst == DataTypeCategory.LINE:
            return viewLine()
        else:
            return DataView()

    def checkGroupType(inst):
        if inst.value == 1:  # 가운데 검은박스 역영
            return DataGroup.GRP_POINTCLOUD
        elif inst.value <= 10:  #
            return DataGroup.GRP_SINGLE_OBJECT
        elif inst.value <= 19:  # display 영역
            return DataGroup.GRP_DISPLAY
        elif inst.value <= 29:  # 20~29번은 text 영역
            return DataGroup.GRP_ETC
