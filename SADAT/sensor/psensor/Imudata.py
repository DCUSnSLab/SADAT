from dadatype.dtype_information import dtype_sensor
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor

class Imudata(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self,inputdata):
        data = dtype_sensor(inputdata)
        self.addRealtimeData(data)