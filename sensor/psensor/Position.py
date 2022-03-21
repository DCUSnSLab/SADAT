from dadatype.dtype_information import dtype_float
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor
import numpy as np
from utils.importer import Importer

class Position(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self,inputdata):#데이터 출력 여기서 원하는 데이터 설정 하기
        data = dtype_float(inputdata)#, tstamp)
        self.addRealtimeData(data)