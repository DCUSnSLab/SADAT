from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer
import sensor_msgs.point_cloud2 as pc2
import ros_numpy

class Velodyne3D(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Lidar3D, name)

    def _doWorkDataInput(self, inputdata):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        pc2 = Importer.importerLibrary('sensor_msgs.point_cloud2')
        #print(inputdata)
        #print(field_names)
        pc = ros_numpy.numpify(inputdata)
        points = np.zeros((pc.shape[0], 3))
        points[:, 0] = pc['x']
        points[:, 1] = pc['y']
        points[:, 2] = pc['z']
        # print(pc[0])
        # print(points[0])
        # # p = pcl.PointCloud(np.array(points,
        tstamp = inputdata.header.stamp
        lgrp = grp_rplidar(points, None, None, tstamp.to_sec(), True)
        self.addRealtimeData(lgrp)