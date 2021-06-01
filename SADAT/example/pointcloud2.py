import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import ros_numpy
import numpy as np

def callback(data):
    field_names = [f.name for f in data.fields]
    #print(field_names)
    #print(data.header)
    now = data.header.stamp
    print(now.secs, now.to_sec())
    pc = ros_numpy.numpify(data)
    points=np.zeros((pc.shape[0],3))
    points[:,0]=pc['x']
    points[:,1]=pc['y']
    points[:,2]=pc['z']
    print('total cnt - ', len(pc), len(points))
    print(points[0], type(points[0]))
    #p = pcl.PointCloud(np.array(points, dtype=np.float32))

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("/velodyne_points", PointCloud2, callback)
rospy.spin()