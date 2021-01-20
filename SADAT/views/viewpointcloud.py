from views.DataView import DataView


class viewPointCloud(DataView):
    def __init__(self, pdata=None):
        super().__init__(rawdata=pdata)