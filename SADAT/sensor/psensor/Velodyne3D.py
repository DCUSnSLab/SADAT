from dadatype.grp_rplidar import grp_rplidar
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer
import sensor_msgs.point_cloud2 as pc2
import ros_numpy
import time

class Velodyne3D(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Lidar3D, name)
        self.prevTime = 0
    def _doWorkDataInput(self, inputdata):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        pc2 = Importer.importerLibrary('sensor_msgs.point_cloud2')
        #print(inputdata)
        field_names = [f.name for f in inputdata.fields]
        #print(field_names)
        pc = ros_numpy.numpify(inputdata)
        # datasize = 5000
        # points = np.zeros((datasize, 3))
        # points[:datasize, 0] = pc['x'][:datasize]
        # points[:datasize, 1] = pc['y'][:datasize]
        # points[:datasize, 2] = pc['z'][:datasize]
        points = np.zeros((pc.shape[0], 4))
        points[:, 0] = pc['x']
        points[:, 1] = pc['y']
        points[:, 2] = pc['z']
        points[:, 3] = pc['intensity']
        #print(len(points))
        # print(pc[0])
        # print(points[0])
        # # p = pcl.PointCloud(np.array(points,
        tstamp = inputdata.header.stamp
        lgrp = grp_rplidar(points, None, None, tstamp.to_sec(), True)

        curTime = time.time()
        sec = curTime - self.prevTime
        self.prevTime = curTime
        fps = 1 / (sec)
        #print(len(pc), 'fps - ', fps)
        self.addRealtimeData(lgrp)