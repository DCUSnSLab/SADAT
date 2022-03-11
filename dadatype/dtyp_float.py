from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_float(DataWrapper):
    def __init__(self, speedfloat):  # timestamp 추가 하면 추가됨
        super().__init__(id=0, dtypecate=DataTypeCategory.Float)  # , timestamp=timestamp)
        self.speedfloat = speedfloat