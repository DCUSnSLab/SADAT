from grabber.Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog
from sensor.SenAdptMgr import AttachedSensorName
from sensor.SourceManager import SourceManager
from utils.sadatlogger import slog
from dadatype.grp_pointclouds import grp_pointclouds

import os, math, pcl
import numpy as np

class LogSimDispatcher(Dispatcher):

    def __init__(self, srcmgr:SourceManager, opensrc=""):
        super().__init__()
        self.sourcemanager = srcmgr
        self.opensrc = opensrc
        slog.DEBUG("LogSimDispatcher Init")

    def dispatch(self):
        self.loadData()
        self.logDispatch()
        self.sendEvent()

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
        return np.array(cmap)

    def loadData(self):
        slog.DEBUG("-----lodata method called-----")
        print(os.getcwd())

        if self.opensrc == "":
            self.opensrc = "../Data/data_1.dat"
            #self.opensrc = "../data/bunny.pcd"장

        #파일을 저장할 때 head 부분에 디바이스 네임을 작성해줘야함
        #헤더파일의 디바이스 네임에 따라 rawdata에 저장될 수 있도록 변경해야함
        lidarlog = makeRPLidarLog(self.opensrc)
        self._rawdata[AttachedSensorName.RPLidar2DVirtual] = lidarlog.fromlogFile()

        cloud = pcl.load_XYZI("../Data/20211104_map.pcd")
        # cloud = pcl.load("../../../bunny.pcd")

        np_cloud = cloud.to_array()

        cmap = self.__make_colormap()
        '''
        임의로 구현한 makeRPLidarLog와 같은 클래스를 통해 .pcd 확장자 파일에서 데이터를 불러오고,
        읽어들인 데이터를 self._rawdata[연결된 센서 이름] 에 저장해야 한다.
        
        불러오는 과정의 경우 
        '''
        # lidarlog = makeRPLidarLog(self.opensrc)
        #self._rawdata[AttachedSensorName.VelodyneVLC16] = self.lgrp

    def logDispatch(self):
        for scate in self._rawdata.keys():
            if scate in self.sourcemanager.AllSensors.keys():
                val = self._rawdata[scate]
                sensor = self.sourcemanager.AllSensors[scate]
                sensor.doWork(val)
        slog.DEBUG("Data Load Finished")

    def sendEvent(self):
        slog.DEBUG("send Event")
        loadedsens = list()
        # send event to taskLoopPlay to wake up sim receive module
        for data in self._rawdata.keys():
            loadedsens.append(data)
        self.sourcemanager.simEvent(loadedsens)
