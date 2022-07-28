import math
import pcl

from dadatype.grp_pointclouds import grp_pointclouds
from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor
import numpy as np
from utils.importer import Importer

class Velodyne3Dv(vSensor):
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
        # print(color)
        cmap = [self.num_to_rgb(color[i], maxval) for i in range(len(color))]
        self.cmap = np.array(cmap)

    def _doWorkDataInput(self, inputdata):
        """
        Args:
            inputdata: PCL PointCloud 데이터

        Returns:
            None
        """
        points = np.zeros((inputdata.shape[0], 7))

        points[:, 0] = inputdata[:, 0]
        points[:, 1] = inputdata[:, 1]
        points[:, 2] = inputdata[:, 2]
        points[:, 3] = inputdata[:, 3]

        points[:, 3:7] = 0.9

        self.lgrp = grp_pointclouds(points, None, None, 0.0, True)

        # curTime = time.time()
        # sec = curTime - self.prevTime
        # self.prevTime = curTime
        # fps = 1 / (sec)
        # print(len(pc), 'fps - ', fps)

        self._addSimData(self.lgrp)
        print()
        print("storedData")
        print()
        print(self.storedData)
        print(type(self.storedData))

    def __resamplePoints(self, points, size=None):
        # re sampling pointcloud for performance
        # default value = None
        if size is not None:
            idx = np.random.randint(len(points), size=10000)
            points = points[idx, :]
        return points