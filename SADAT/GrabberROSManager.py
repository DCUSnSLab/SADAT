from enum import Enum

from utils.importer import Importer

# class ROSGrabberList(Enum):
#     ROS_RPLIDAR = GrabberROSrplidar()


class grabberROSManager:
    def __init__(self):
        try:
            self.rospy = Importer.importerLibrary('rospy')
        except:
            self.rospy = None

        print('rosmanager - ',self.rospy.get_published_topics())