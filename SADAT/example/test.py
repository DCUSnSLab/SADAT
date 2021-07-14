import rospy
from sensor_msgs.msg import PointCloud2, CompressedImage
import sensor_msgs.point_cloud2 as pc2
import ros_numpy
import numpy as np
import time

from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer

print('-----published topic lists-----')
topic_lists = dict()
for data in rospy.get_published_topics():
    msgs = data[1].split('/')
    from_str = msgs[0] + '.msg'
    import_str = msgs[1]
    msg = Importer.importerLibrary(from_str, import_str)
    topic_lists[data[0]] = msg

print(topic_lists)
print(AttachedSensorName.__dict__['_value2member_map_'])
enum_list = list(map(AttachedSensorName, AttachedSensorName))
for i in enum_list:
    print(i.value)
#print(enum_list)  # prints [1, 2]
