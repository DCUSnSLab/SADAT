#센서 데이터 생성
from dadatype.dtype_information import dtype_float
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor


class SPFloat(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self, inputdata):#데이터 출력 여기서 원하는 데이터 설정 하기
        # print(inputdata)
        #tstamp = float(inputdata.header.stamp.to_sec())
        data = dtype_float(inputdata)#, tstamp)
        self.addRealtimeData(data)