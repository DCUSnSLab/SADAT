from dadatype.dtype_cate import DataTypeCategory
from externalmodules.default.dataset_enum import senarioBasicDataset
from views.viewpointcloud import viewPointCloud

class guiInfo():
    def __init__(self, planviewsize, wwidth, wheight, relx, rely):
        self.planviewsize = planviewsize
        self.wwidth = wwidth
        self.wheight = wheight
        self.relx = relx
        self.rely = rely

class planviewManager():
    def __init__(self):
        self.objects = dict()
        self.guiinfo = None

    def updateview(self, inputs):
        for ikey, ivalues in inputs.items():
            if ikey != 'rawdata': #temporary
                self.objects[ikey] = self.__addView(ivalues)

    def updateposinfo(self, guiinfo):
        self.guiinfo = guiinfo

    def updateAllpos(self, guiinfo):
        self.updateposinfo(guiinfo)
        for object in self.objects.values():
            for objitem in object:
                objitem.updatePlanviewPos(guiinfo)

    #match the view with data of dtype using dtypecategory
    def __addView(self, values):
        templist = list()
        for item in values:
            tempitem = DataTypeCategory.getInstance(DataTypeCategory[item.dtypecate.name])
            tempitem.initView(item)
            tempitem.updatePlanviewPos(self.guiinfo)
            templist.append(tempitem)
        return templist

    def getObjectList(self):
        return list(self.objects.keys())

    def getObject(self, key):
        if key in self.objects:
            return self.objects[key]
        else:
            return None

    def getObjects(self):
        return self.objects.items()

