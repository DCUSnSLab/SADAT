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

        #add vispy scene
        # self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True, bgcolor='#000d1a')
        # self.view = self.canvas.central_widget.add_view()
        # axis = visuals.XYZAxis(parent=self.view.scene)
        # grid1 = visuals.GridLines(parent=self.view.scene, scale=(5,5))
        # self.view.camera = TurntableCamera(fov=30.0, elevation=90.0, azimuth=-90.0, distance=100, translate_speed=50.0)

        #add pyqtgraph
        self.canvas = pg.GraphicsLayoutWidget()
        hbox.addWidget(self.canvas)
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.disableAutoRange()
        #self.view.setRange(QtCore.QRectF(0, 0, 100, 100))

        # Generate random points
        # n = 1000
        # print('Number of points: ' + str(n))
        # data = np.random.normal(size=(2, n))
        # pos = [{'pos': data[:, i]} for i in range(n)]
        #
        # self.sp.setData(pos)

        #add ego vehicle
        self.drawEgoVehicle()

        #draw objects
        self.draw()

    def drawEgoVehicle(self):
        pass
        #r1 = pg.QtGui.QGraphicsRectItem(0, 0, 0.4, 1)
        #r1.setPen(pg.mkPen(None))
        #r1.setBrush(pg.mkBrush('r'))
        #self.view.addItem(r1)
        # box = visuals.Box(width=1, height=1, depth=1, color=(0.5, 0.5, 1, 0), edge_color='white')
        # # box.transform = MatrixTransform()
        # box.transform = transforms.STTransform(translate=(0., 0., 0.), scale=(0.7, 0.35, 0.2))
        # self.view.add(box)

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
            #print(color[:,:3])
            #print(pos[:,3])
            #cm = pg.colormap.get('jet', source='matplotlib')
            #cm.map(pos[:,3], mode=ColorMap.FLOAT)
            #brush = cm.getPen()
            viewitem.setData(pos=pos)
            #viewitem.setBrush(color)
        elif dataview.viewType == DataTypeCategory.TRACK:
            pass
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
                il[id] = it
                self.view.addItem(it)

            #set Visible Mode Changer
            self.isOnceExeInvMode[key] = False

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            sp = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='r'), symbol='o', size=2)
            return sp, dataview.rawid
        elif dataview.viewType == DataTypeCategory.TRACK: #Track Visual 부분을 Box 말고 다른 view로 바꿔봐야할 것 같음...
            sp = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='r'), symbol='o', size=1)
            return sp, dataview.rawid
            #return visuals.Markers(edge_color=None, size=10, symbol='square'), dataview.rawid
        else: #need to add line
            return None