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

    #update data to display on planview
    #All objects which are rawdata(DataTypeCategory) and externaldataset(ex. senarioBasicDataset) are updated and associated in 'objects' value in planviewmanager
    def updateview(self, inputs):
        for rkey, rval in inputs.items():
            ispc, value = self.__checkPointCloud(rval)
            self.objects[rkey] = self.__addView(rval, ispc)

    def updateposinfo(self, guiinfo):
        self.guiinfo = guiinfo


    #이 부분 체크해서 이 함수 밑에 드로우 함수 만들기
    def updateAllpos(self, guiinfo):
        self.updateposinfo(guiinfo)
        for object in self.objects.values():
            for objitem in object:
                objitem.updatePlanviewPos(guiinfo)

    def draw(self,qp):
        pass

    #match the view with data of dtype using dtypecategory
    def __addView(self, values, isPointCloud):
        templist = list()
        if isPointCloud:
            if isinstance(values, list):
                for item in values:
                    self.__addViewItem(templist, item)
            else:
                self.__addViewItem(templist, values)
        else:
            for item in values:
                self.__addViewItem(templist, item)

        return templist

    def __addViewItem(self, vlist, item):
        tempitem = DataTypeCategory.getInstance(DataTypeCategory[item.dtypecate.name])
        tempitem.initView(item)
        tempitem.updatePlanviewPos(self.guiinfo)
        vlist.append(tempitem)

    def __checkPointCloud(self, val):
        objval = None
        ispc = False
        if isinstance(val, list) and len(val) == 0:
            return False, val
        elif isinstance(val, list):
            objval = val[0]
        else:
            objval = val

        if objval.dtypecate == DataTypeCategory.POINT_CLOUD:
            ispc = True
        else:
            ispc = False

        return ispc, objval

    def getObjectList(self):        #key값 가져옴
        return list(self.objects.keys())

    def getObject(self, key):
        if key in self.objects:
            return self.objects[key]
        else:
            return None

    def getObjects(self):
        return self.objects.items()

