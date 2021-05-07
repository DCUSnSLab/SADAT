from enum import Enum

from utils.importer import Importer

# class ROSGrabberList(Enum):
#     ROS_RPLIDAR = GrabberROSrplidar()
from utils.sadatlogger import slog


class grabberROSManager:
    def __init__(self):
        try:
            self.rospy = Importer.importerLibrary('rospy')
            slog.DEBUG('-----published topic lists-----')
            for data in self.rospy.get_published_topics():
                slog.DEBUG(data)
        except:
            self.rospy = None

