import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import ros_numpy
import numpy as np
import time

prevTime = 0

def callback(data):
    global prevTime
    field_names = [f.name for f in data.fields]
    #print(field_names)
    #print(data.header)

    pc = ros_numpy.numpify(data)
    #points=np.zeros((pc.shape[0],3))
    #points[:,0]=pc['x']
    #points[:,1]=pc['y']
    #points[:,2]=pc['z']
    #print('total cnt - ', len(pc), len(points))
    #print(points[0], type(points[0]))

    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / (sec)
    print(len(pc), 'fps - ',fps)
    #p = pcl.PointCloud(np.array(points, dtype=np.float32))

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("/velodyne_points", PointCloud2, callback)
rospy.spin()