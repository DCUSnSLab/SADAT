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
        #self.opensrc = "../Data/20211104_map.pcd"
        #self.opensrc = "/home/ros/pcd_data/20211110_res_0.09.pcd"
        self.opensrc = "/home/ros/pcd_data/20211110_res_0.95.pcd"
        #self.opensrc = "../Data/bunny.pcd"
        # self.opensrc = opensrc
        slog.DEBUG("LogSimDispatcher Init")

    def dispatch(self):
        # 해당 함수에서 누른 버튼에 따라 다른 데이터를 로드하도록 수정 필요??
        # 우선은 QWidget을 통해 파일 경로를 명시할 수 없는 버그를 수정하는게 우선임

        self.loadData()
        self.logDispatch()
        self.sendEvent()

    def loadData(self):
        slog.DEBUG("-----loadData method called-----")
        print(os.getcwd())

        #if self.opensrc == "":
            #self.opensrc = "../Data/data_1.dat"
            #self.opensrc = "../data/bunny.pcd"장

        #파일을 저장할 때 head 부분에 디바이스 네임을 작성해줘야함
        #헤더파일의 디바이스 네임에 따라 rawdata에 저장될 수 있도록 변경해야함
        #lidarlog = makeRPLidarLog(self.opensrc)
        VLPlidarlog = makeVLPLog(self.opensrc)
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

    def setFilesrc(self, opensrc):
        slog.DEBUG("setFilesrc called.")
        self.opensrc = opensrc
        self.dispatch()
