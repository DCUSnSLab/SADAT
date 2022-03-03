from dadatype.dtype_cate import DataTypeCategory
from externalmodules.default.dataset_enum import senarioBasicDataset
from sensor.SenAdptMgr import AttachedSensorName
from utils.sEventHandler import sEventHandler
from views.viewpointcloud import viewPointCloud

class guiInfo():
    def __init__(self, planviewsize, wwidth, wheight, relx, rely):
        self.planviewsize = planviewsize
        self.wwidth = wwidth
        self.wheight = wheight
        self.relx = relx
        self.rely = rely

class planviewManager():
    visibleChanged = sEventHandler()
    def __init__(self):
        self.objects = dict()
        self.pObjkeycnt = 0
        self.objectVisible = dict()

    #update data to display on planview
    #All objects which are rawdata(DataTypeCategory) and externaldataset(ex. senarioBasicDataset) are updated and associated in 'objects' value in planviewmanager
    def updateview(self, inputs):
        for rkey, rval in inputs.items():
            isgobj, value = self.__checkGroupObject(rval)
            self.objects[rkey] = self.__addView(rval, isgobj)
        self.objValidate()


    def updateAllpos(self):
        #self.updateposinfo(guiinfo)
        for object in self.objects.values():
            for objitem in object:
                objitem.updatePlanviewPos()

    def draw(self,qp):
        pass

    #match the view with data of dtype using dtypecategory
    def __addView(self, values, isGroupObject):
        templist = list()
        if isGroupObject:
            if values.isPointCloud():
            # if isinstance(values, list):
            #     for item in values:
            #         self.__addViewItem(templist, item)
            # else:
                self.__addViewItem(templist, values)
            else:
                for object in values.getObjects():
                    self.__addViewItem(templist, object)
        else:
            for item in values:
                self.__addViewItem(templist, item)

        return templist

    def __addViewItem(self, vlist, item):
        tempitem = DataTypeCategory.getInstance(DataTypeCategory[item.dtypecate.name])
        tempitem.initView(item)
        vlist.append(tempitem)

    def __checkGroupObject(self, val):
        objval = None
        isgroupobject = False
        if isinstance(val, list) and len(val) == 0:
            return False, val
        elif isinstance(val, list):
            objval = val[0]
            isgroupobject = False
        else:
            objval = val
            isgroupobject = True

        # if objval.dtypecate == DataTypeCategory.POINT_CLOUD:
        #     ispc = True
        # else:
        #     ispc = False

        return isgroupobject, objval

    def getObjectList(self):        #key값 가져옴
        return list(self.objects.keys())

    def getObject(self, key):
        if key in self.objects:
            return self.objects[key]
        else:
            return None

    def getObjects(self):
        return self.objects.items()

    def getObjectVisibility(self, key):
        if key in self.objectVisible:
            return self.objectVisible[key]
        else:
            return False

    def objValidate(self):
        cobjcnt = len(self.objects)

        if self.pObjkeycnt < cobjcnt:
            #revalidate object visibility list
            for objkey in self.getObjectList():
                if (objkey in self.objectVisible) is False:
                    self.objectVisible[objkey] = True
            self.visibleChanged.trigger(self.objectVisible)
            self.pObjkeycnt = cobjcnt
