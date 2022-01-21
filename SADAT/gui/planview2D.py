from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtGui
import numpy as np
from pyqtgraph import ColorMap
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
from dadatype.dtype_cate import DataTypeCategory


class planView2D(QWidget):
    def __init__(self, planviewmanager):
        super().__init__()
        self.isOnceExeInvMode = dict()
        self.cnt = 0
        #set planview manager
        self.pvmanager = planviewmanager
        #view item list
        self.itemlist = dict()
        hbox = QHBoxLayout()

        #add pyqtgraph
        self.canvas = pg.GraphicsLayoutWidget()
        hbox.addWidget(self.canvas)
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.disableAutoRange()
        #self.view.setRange(QtCore.QRectF(0, 0, 100, 100))

        grid = pg.GridItem()
        self.view.addItem(grid)
        #add ego vehicle
        self.drawEgoVehicle()

        #draw objects
        self.draw()

    def drawEgoVehicle(self):
        pass
        ev = pg.QtGui.QGraphicsRectItem(-0.175, -0.35, 0.35, 0.7)
        ev.setPen(pg.mkPen(None))
        ev.setBrush(pg.mkBrush('r'))
        self.view.addItem(ev)

    def draw(self):
        for ikey, values in self.pvmanager.getObjects():
            self.updateItems(ikey, values)

            isvisible = self.pvmanager.getObjectVisibility(ikey)
            for i, idata in enumerate(values):
                pos, size, color = idata.draw(ikey, True)
                if self.itemlist[ikey].get(idata.rawid) is None:
                    continue
                elif isvisible:
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
            viewitem.setData(pos=pos)
        elif dataview.viewType == DataTypeCategory.TRACK:
            viewitem.setRect((pos[1]*-1)-0.5, pos[0]-0.5, size[1], size[0])
        elif dataview.viewType == DataTypeCategory.LINE:
            pass
        elif dataview.viewType == DataTypeCategory.LANE:
            pass

    def __drawInvisible(self, viewitem, dataview, pos, size, color):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            viewitem.set_data(pos=np.array([[0,0,0]]),size=0)
        elif dataview.viewType == DataTypeCategory.TRACK:
            viewitem.border.color = (1, 1, 1, 0)

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
                if it is not None:
                    il[id] = it
                    self.view.addItem(it)

            #set Visible Mode Changer
            self.isOnceExeInvMode[key] = False

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            sp = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='r'), symbol='o', size=2)
            return sp, dataview.rawid
        elif dataview.viewType == DataTypeCategory.TRACK: #Track Visual 부분을 Box 말고 다른 view로 바꿔봐야할 것 같음...
            #tr = pg.QtGui.QGraphicsRectItem(-0.175, -0.35, 0.35, 0.7)
            tr = pg.QtGui.QGraphicsRectItem(-0.5, -0.5, 0.5, 0.5)
            tr.setPen(pg.mkPen('w'))
            return tr, dataview.rawid
        else: #need to add line
            return None