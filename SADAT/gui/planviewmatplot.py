from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from dadatype.dtype_cate import DataTypeCategory


class planViewMatplot(QWidget):
    def __init__(self, planviewmanager):
        super().__init__()
        self.isOnceExeInvMode = dict()
        self.cnt = 0
        #set planview manager
        self.pvmanager = planviewmanager
        #view item list
        self.itemlist = dict()
        hbox = QHBoxLayout(self)

        self.canvas = FigureCanvas(Figure())
        self.canvas.figure.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0.2, wspace=0.2)
        hbox.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots(sharex=True, sharey=True)
        self.ax.set_facecolor('#000d1a')
        self.ax.set_position([0.0, 0.0, 1, 1])
        self.ax.margins(0)
        self.scatt = self.ax.scatter([0], [0], s=1)
        self.ax.set_xlim(-40, 40)
        self.ax.set_ylim(-40, 40)
        self.ax.invert_xaxis()
        self.timer = self.canvas.new_timer(
            1, [(self.draw, (), {})])
        self.timer.start()
        #hbox.addWidget(self.canvas.native)
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)
        #self.draw()

    def draw(self):
        for ikey, values in self.pvmanager.getObjects():
            self.updateItems(ikey, values)
            isvisible = self.pvmanager.getObjectVisibility(ikey)
            for i, idata in enumerate(values):
                pos, size, color = idata.draw(ikey, True)
                if isvisible:
                    self.__drawVisible(self.itemlist[ikey][idata.rawid], idata, pos, size, color)
                    #self.itemlist[ikey][idata.rawid].set_data(pos=pos[:,:3], face_color=color, size=2, edge_color=color)
                else:
                    if self.isOnceExeInvMode[ikey] is False:
                        self.__drawInvisible(self.itemlist[ikey][idata.rawid], idata, pos, size, color)
                    #self.itemlist[ikey][idata.rawid].set_data(pos=np.array([[0,0,0]]),size=0)

            if isvisible is False and self.isOnceExeInvMode[ikey] is False:
                self.isOnceExeInvMode[ikey] = True
            elif isvisible is True:
                self.isOnceExeInvMode[ikey] = False



    def __drawVisible(self, viewitem, dataview, pos, size, color):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            self.scatt.set_offsets(pos[:, :2])
            #self.ax.figure.canvas.draw()
            #pass
            #viewitem.set_data(pos=pos[:, :3], face_color=color, size=2, edge_color=color)
        elif dataview.viewType == DataTypeCategory.TRACK:
            pass
            # viewitem.transform.reset()
            # viewitem.transform.scale(size)
            # viewitem.transform.translate(pos)
        elif dataview.viewType == DataTypeCategory.LINE:
            pass
        elif dataview.viewType == DataTypeCategory.LANE:
            pass

    def __drawInvisible(self, viewitem, dataview, pos, size, color):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            pass
            #viewitem.set_data(pos=np.array([[0,0,0]]),size=0)
        elif dataview.viewType == DataTypeCategory.TRACK:
            pass
            #viewitem.transform.reset()
            #viewitem.transform.scale((0.1,0.1,0.1))
        elif dataview.viewType == DataTypeCategory.LINE:
            pass
        elif dataview.viewType == DataTypeCategory.LANE:
            pass

    def updateItems(self, key, values):
        if (key in self.itemlist) is False:
            self.itemlist[key] = dict()
            il = self.itemlist[key]
            for i, item in enumerate(values):
                it, id = self.applyGLObject(item)
                il[id] = it

                #add plot in Figure
                #self.view.add(it)

            #set Visible Mode Changer
            self.isOnceExeInvMode[key] = False

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            return None, dataview.rawid
            #return visuals.Markers(edge_color=None, size=2), dataview.rawid
        elif dataview.viewType == DataTypeCategory.TRACK: #Track Visual 부분을 Box 말고 다른 view로 바꿔봐야할 것 같음...
            # box = visuals.Box(width=1, height=1, depth=1, color=(0.5, 0.5, 1, 0), edge_color='white')
            # box.transform = MatrixTransform()
            # return box, dataview.rawid
            return None, dataview.rawid
        else: #need to add line
            return None
