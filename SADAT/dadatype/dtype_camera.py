import copy

from dadatype.datawrapper import DataWrapper
from dadatype.dtype_cate import DataTypeCategory


class dtype_camera(DataWrapper):
    def __init__(self, imagedata, timestamp):
        super().__init__(id=0, dtypecate=DataTypeCategory.CAMERA, timestamp=timestamp)
        self.imagedata = imagedata