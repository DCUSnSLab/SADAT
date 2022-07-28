import numpy as np
import pcl
from log.makeLog import makeLog
from utils.sadatlogger import slog
from numpy import fromfile

# PointCloud 데이터 출력을 위한 로그 생성 파일
# 해당 파일에서는 pcl 라이브러리를 통한 데이터 로드 후
# ros_numpy
# 불러온 데이터를 SADAT에서 출력할 수 있는 형태로 정제하는 과정은
# SADAT/SADAT/sensor/vsensor/Velodyne3Dv.py 에서 수행한다.

class makeVLPLog(makeLog):
    def __init__(self, filename):
        slog.DEBUG("-----makeVLP16Log __init__ method called-----")
        self.cloud = None
        self.np_cloud = None
        super().__init__(filename)

    def logData(self, loggingdata=None):
        pass

    def setFilesrc(self, opensrc):
        slog.DEBUG("setFilesrc called.")
        self.filename = opensrc

    def fromlogFile(self):
        """
        생성자 필드로 존재하는 filename을 사용하여 cloud 데이터를 불러오고,
        불러온 데이터가 기존 self.cloud와 동일한 데이터인지 확인 후 동일한 경우 유지,
        다른 경우 새로 불러오는 과정을 수행한다.
        """
        slog.DEBUG("-----makeVLP16Log fromlogFile method called-----")

        self.cloud = pcl.load_XYZI(self.filename)
        # load_XYZI() 함수를 사용하여 데이터를 불러오는 경우 intensity 필드를 못 찾는 상황에 대하여 예외처리가 필요하다.
        self.np_cloud = self.cloud.to_array()

        return self.np_cloud