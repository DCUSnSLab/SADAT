from grabber.Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog
from log.makeVLP16Log import makeVLPLog
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
        # 해당 함수에서 누른 버튼에 따라 다른 데이터를 로드하도록 수정 필요??
        # 우선은 QWidget을 통해 파일 경로를 명시할 수 없는 버그를 수정하는게 우선임

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
        #lidarlog = makeRPLidarLog(self.opensrc)
        VLPlidarlog = makeVLPLog("../Data/20211104_map.pcd")
        #self._rawdata[AttachedSensorName.RPLidar2DVirtual] = lidarlog.fromlogFile()
        self._rawdata[AttachedSensorName.StaticPointCloudVirtual] = VLPlidarlog.fromlogFile()

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
