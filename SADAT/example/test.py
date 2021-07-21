import cv2
import rospy
from sensor_msgs.msg import PointCloud2, CompressedImage
import sensor_msgs.point_cloud2 as pc2
import ros_numpy
import numpy as np
import time

from sensor.SenAdptMgr import AttachedSensorName
from utils.importer import Importer

def callback(msg):
    data = msg
    topic = data._connection_header['topic']
    type = data._connection_header['type']
    data1 = 1
    ros_numpy = Importer.importerLibrary('ros_numpy')
    pc2 = Importer.importerLibrary('sensor_msgs.point_cloud2')
    pc = ros_numpy.numpify(msg)
    points = np.zeros((pc.shape[0], 7))
    points[:, 0] = pc['x']
    points[:, 1] = pc['y']
    points[:, 2] = pc['z']
    points[:, 3] = pc['intensity']
    inten = pc['intensity'].astype(np.int32)
    #color = np.array([1 for i in range(len(inten))])
    #points[:, 3:7] = color[:, 0:4]
    tstamp = msg.header.stamp
    #print('lidar is done')

def callbackcam(msg):
    cv_image = None
    inputdata = msg

    # np_arr = np.fromstring(msg.data, np.uint8)
    # cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
    # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    #
    # tstamp = float(inputdata.header.stamp.to_sec())
    # h, w, ch = cv_image.shape


print('-----published topic lists-----')
topic_lists = dict()
pdata = rospy.get_published_topics()
for data in rospy.get_published_topics():
    msgs = data[1].split('/')
    from_str = msgs[0] + '.msg'
    import_str = msgs[1]
    msg = Importer.importerLibrary(from_str, import_str)
    topic_lists[data[0]] = msg

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("/velodyne_points", PointCloud2, callback)
rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, callbackcam)
rospy.spin()
rospy.spin()


#print(enum_list)  # prints [1, 2]
