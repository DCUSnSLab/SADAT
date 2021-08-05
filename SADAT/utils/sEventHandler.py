class sEventHandler():
    def __init__(self):
        self.hfunc = None

    def trigger(self, obj):
        self.hfunc(obj)
