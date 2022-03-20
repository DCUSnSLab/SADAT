#센서 데이터 생성
from dadatype.dtype_imformation import dtype_Odometry
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer

class Odom(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self, inputdata):#데이터 출력 여기서 원하는 데이터 설정 하기
        # print(inputdata)
        #tstamp = float(inputdata.header.stamp.to_sec())
        data = dtype_Odometry(inputdata)#, tstamp)
        self.addRealtimeData(data)