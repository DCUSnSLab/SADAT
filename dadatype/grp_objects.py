from dadatype.datawrapper import DataWrapper


class grp_objects(DataWrapper):
    def __init__(self, dtypecate, timestamp):
        super().__init__(id=0, dtypecate=dtypecate, timestamp=timestamp, isgroupobject=True)
        self.__objects = list()

    def addObject(self, obj):
        self.__objects.append(obj)

    def addObjects(self, objs):
        self.__objects = objs

    def getObjects(self):
        return self.__objects


