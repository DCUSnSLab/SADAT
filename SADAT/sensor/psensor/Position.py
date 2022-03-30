from dadatype.dtype_information import dtype_float
from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor

class Position(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.ESC, name)

    def _doWorkDataInput(self,inputdata):
        data = dtype_float(inputdata)
        self.addRealtimeData(data)