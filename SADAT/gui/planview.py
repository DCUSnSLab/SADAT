from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from pyqtgraph.opengl import GLScatterPlotItem, GLMeshItem

from dadatype.dtype_cate import DataTypeCategory


class planView(QWidget):
    def __init__(self, planviewmanager):
        super().__init__()
        self.cnt = 0
        #set planview manager
        self.pvmanager = planviewmanager
        #view item list
        self.itemlist = dict()
        hbox = QHBoxLayout()
        self.glwidget = gl.GLViewWidget()
        self.glwidget.setBackgroundColor((0,0,0))
        self.glwidget.opts['distance'] = 100
        hbox.addWidget(self.glwidget)
        self.setLayout(hbox)

        gv = gl.GLGridItem()
        gv.setSize(size=QtGui.QVector3D(300,300,1))
        gv.setSpacing(10,10,0)
        self.glwidget.addItem(gv)

        self.draw()

    def draw(self):
        for ikey, values in self.pvmanager.getObjects():
            self.addItems(ikey, values)
            for i, idata in enumerate(values):
                pos, color = idata.draw(ikey, True)
                self.itemlist[ikey][i].setData(pos=pos, color=color)

    def addItems(self, key, values):
        if (key in self.itemlist) is False:
            self.itemlist[key] = list()
            il = self.itemlist[key]
            for item in values:
                it = self.applyGLObject(item)
                il.append(it)
                self.glwidget.addItem(it)
            #self.itemlist.append(key)

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            return GLScatterPlotItem(size=0.25, pxMode=False)
        else:
            return None
    # def draw(self):
    #     self.glwidget.clear()
    #     ts = [[1.0, 1.0, 0.0], [10.0, 10.0, 10.0], [1000, 10, 10]]
    #     pts = np.random.random(size=(3, 3))
    #     pts *= [10, -10, 0]
    #     color = [pg.glColor((255, 0, 0, 255)), pg.glColor((0, 255, 0, 255)), pg.glColor((0, 0, 255, 255))]
    #     pts = np.array(pts)
    #     color = np.array(color)
    #     # print(pts)
    #     # print(color)
    #     gv = gl.GLGridItem()
    #     gv.setSize(100, 100, 100)
    #     self.glwidget.addItem(gv)
    #     plt = gl.GLScatterPlotItem(pos=pts, color=color, size=1, pxMode=False)
    #     self.glwidget.addItem(plt)
