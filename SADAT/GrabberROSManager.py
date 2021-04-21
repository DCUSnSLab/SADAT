from enum import Enum

from utils.importer import Importer

# class ROSGrabberList(Enum):
#     ROS_RPLIDAR = GrabberROSrplidar()


class grabberROSManager:
    def __init__(self):
        self.rospy = Importer.importerLibrary('rospy')
        print('rosmanager - ',self.rospy.get_published_topics())