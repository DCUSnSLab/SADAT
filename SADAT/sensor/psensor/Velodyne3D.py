import math

from dadatype.grp_pointclouds import grp_pointclouds
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer

class Velodyne3D(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Lidar3D, name)
        self.prevTime = 0
        self.cmap = None
        self.__make_colormap()

    def num_to_rgb(self, val, max_val=141):
        rgb = 255
        i = (val * 255 / max_val);
        r = math.sin(0.024 * i + 0) * 127 + 128
        g = math.sin(0.024 * i + 2) * 127 + 128
        b = math.sin(0.024 * i + 4) * 127 + 128
        return [r / rgb, g / rgb, b / rgb, 1]

    def __make_colormap(self):
        res = 1
        maxval = 256
        cnt = maxval * res
        color = [i * (1 / res) for i in range(cnt)]
        #print(color)
        cmap = [self.num_to_rgb(color[i], maxval) for i in range(len(color))]
        self.cmap = np.array(cmap)

    def _doWorkDataInput(self, inputdata):
        ros_numpy = Importer.importerLibrary('ros_numpy')
        #pc2 = Importer.importerLibrary('sensor_msgs.point_cloud2')
        pc = ros_numpy.numpify(inputdata)
        points = np.zeros((pc.shape[0], 7))

        #for ROS and vehicle, x axis is long direction, y axis is lat direction
        points[:, 0] = pc['x']
        points[:, 1] = pc['y']
        points[:, 2] = pc['z']
        points[:, 3] = pc['intensity']
        inten = pc['intensity'].astype(np.int32)
        color = np.array([self.cmap[inten[i]] for i in range(len(inten))])
        points[:, 3:7] = color[:, 0:4]

        #re sampling pointcloud for performance
        points = self.__resamplePoints(points, 10000)

        tstamp = inputdata.header.stamp
        self.lgrp = grp_pointclouds(points, None, None, tstamp.to_sec(), True)

        #curTime = time.time()
        #sec = curTime - self.prevTime
        #self.prevTime = curTime
        #fps = 1 / (sec)
        #print(len(pc), 'fps - ', fps)
        self.addRealtimeData(self.lgrp)

    def __resamplePoints(self, points, size=None):
        # re sampling pointcloud for performance
        # default value = None
        if size is not None:
            idx = np.random.randint(len(points), size=10000)
            points = points[idx, :]
        return points
