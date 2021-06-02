import math

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
        self.cmap = None
        self.__make_colormap()

    def num_to_rgb(self, val, max_val=141):
        i = (val * 255 / max_val);
        r = math.sin(0.024 * i + 0) * 127 + 128
        g = math.sin(0.024 * i + 2) * 127 + 128
        b = math.sin(0.024 * i + 4) * 127 + 128
        return [r / 255, g / 255, b / 255, 1]

    def __make_colormap(self):
        res = 1
        maxval = 256
        cnt = maxval * res
        color = [i * (1 / res) for i in range(cnt)]
        print(color)
        cmap = [self.num_to_rgb(color[i], maxval) for i in range(len(color))]
        self.cmap = np.array(cmap)

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
        points = np.zeros((pc.shape[0], 7))
        points[:, 0] = pc['x']
        points[:, 1] = pc['y']
        points[:, 2] = pc['z']
        points[:, 3] = pc['intensity']
        inten = pc['intensity'].astype(np.int32)
        #inten = b[:, 3].astype(np.int32)
        #print('min:',inten.min(), 'max:',inten.max())
        color = np.array([self.cmap[inten[i]] for i in range(len(inten))])
        #color = [self.num_to_rgb(inten[i]) for i in range(len(inten))]
        points[:, 3:7] = color[:, 0:4]
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