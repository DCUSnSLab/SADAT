from dadatype.dtype_imformation import dtype_sensor
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer

class Imudata(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self,inputdata):#데이터 출력 여기서 원하는 데이터 설정 하기
        data = dtype_sensor(inputdata)#, tstamp)
        self.addRealtimeData(data)