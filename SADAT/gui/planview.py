import vispy.scene
from vispy.scene import visuals, TurntableCamera
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtGui
import numpy as np
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

        #add vispy
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        axis = visuals.XYZAxis(parent=self.view.scene)
        grid1 = visuals.GridLines(parent=self.view.scene, scale=(5,5))
        self.view.camera = TurntableCamera(fov=30.0, elevation=90.0, azimuth=0.0, distance=500, translate_speed=100.0)
        hbox.addWidget(self.canvas.native)
        self.setLayout(hbox)

        self.draw()


    def draw(self):
        for ikey, values in self.pvmanager.getObjects():
            self.addItems(ikey, values)
            for i, idata in enumerate(values):
                pos, color = idata.draw(ikey, True)
                self.itemlist[ikey][i].set_data(pos=pos, edge_color=None, face_color=color, size=5)

    def addItems(self, key, values):
        if (key in self.itemlist) is False:
            self.itemlist[key] = list()
            il = self.itemlist[key]
            for item in values:
                it = self.applyGLObject(item)
                il.append(it)
                self.view.add(it)
            #self.itemlist.append(key)

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            return visuals.Markers()
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
