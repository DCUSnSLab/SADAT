from enum import Enum

from views.DataView import DataView
from views.viewpointcloud import viewPointCloud
from views.viewtrack import viewTrack


class DataTypeCategory(Enum):
    POINT_CLOUD = 1
    TRACK = 2
    LANE = 3
    LINE = 4
    TRAFFIC_SIGN = 5

    def getInstance(inst):
        if inst == DataTypeCategory.POINT_CLOUD:
            return viewPointCloud()
        elif inst == DataTypeCategory.TRACK:
            return viewTrack()
        else:
            return DataView()