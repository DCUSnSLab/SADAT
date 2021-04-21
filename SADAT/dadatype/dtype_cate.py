from enum import Enum

from views.DataView import DataView
from views.viewpointcloud import viewPointCloud
from views.viewtrack import viewTrack


class DataGroup(Enum):
    GRP_POINTCLOUD = 1
    GRP_SINGLE_OBJECT = 2
    GRP_DISPLAY = 3


class DataTypeCategory(Enum):
    POINT_CLOUD = 1
    TRACK = 2
    LANE = 3
    LINE = 4
    TRAFFIC_SIGN = 5
    CAMERA = 11

    def getInstance(inst):
        if inst == DataTypeCategory.POINT_CLOUD:
            return viewPointCloud()
        elif inst == DataTypeCategory.TRACK:
            return viewTrack()
        else:
            return DataView()

    def checkGroupType(inst):
        if inst.value == 1:
            return DataGroup.GRP_POINTCLOUD
        elif inst.value <= 10:
            return DataGroup.GRP_SINGLE_OBJECT
        else:
            return DataGroup.GRP_DISPLAY
