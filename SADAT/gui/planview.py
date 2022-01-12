import random

import vispy.scene
from vispy.scene import visuals, TurntableCamera
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtGui
import numpy as np
from vispy.visuals.transforms import MatrixTransform
from vispy.visuals import transforms

from dadatype.dtype_cate import DataTypeCategory


class planView(QWidget):
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
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True, bgcolor='#000d1a')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'arcball'
        axis = visuals.XYZAxis(parent=self.view.scene)
        #grid1 = visuals.GridLines(parent=self.view.scene, scale=(5,5))
        self.view.camera = TurntableCamera(fov=30.0, elevation=90.0, azimuth=-90.0, distance=100, translate_speed=50.0)
        hbox.addWidget(self.canvas.native)
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)

        #add ego vehicle
        self.egobox = None
        self.theta = 45
        self.phi = 0
        self.drawEgoVehicle()

        #draw objects
        self.draw()

    def drawEgoVehicle(self):
        #self.egobox = visuals.Box(width=0.35, height=0.7, depth=0.2, color=(0.5, 0.5, 1, 0), edge_color='white')
        self.egobox = visuals.Box(width=0.35, height=0.7, depth=0.2, color=(0.5, 0.5, 1, 0), edge_color='white')
        vp = (0, 0, self.canvas.physical_size[0], self.canvas.physical_size[1])
        self.canvas.context.set_viewport(*vp)
        self.egobox.transforms.configure(canvas=self.canvas, viewport=vp)
        # box.transform = MatrixTransform()
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        mt = transforms.MatrixTransform(matrix)
        st = transforms.STTransform(translate=(0., 0., -0.1), scale=(1., 1., 1.))
        self.egobox.transform = transforms.ChainTransform(st, mt)
        self.egobox.transform.transforms[1].reset()
        #self.egobox.transform.transforms[1].scale((2,3,1))
        self.egobox.transform.transforms[1].rotate(90, (1,0,0))
        self.egobox.transform.transforms[1].rotate(90, (0, 0, 1))
        #self.egobox.transform.transforms[1].rotate(45, (0, 0, 1))
        self.view.add(self.egobox)


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
            viewitem.set_data(pos=pos[:, :3], face_color=color, size=2, edge_color=color)
        elif dataview.viewType == DataTypeCategory.TRACK:
            viewitem.transform.transforms[0].translate = pos
            #viewitem.transform.transforms[0].scale = size
            #viewitem.transform.transforms[1].rotate(1, (0, 0, 1))
            if viewitem.border.color.alpha == 0:
                viewitem.border.color = (1, 1, 1, 1)
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
                self.view.add(it)

            #set Visible Mode Changer
            self.isOnceExeInvMode[key] = False

    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            return visuals.Markers(edge_color=None, size=2), dataview.rawid
        elif dataview.viewType == DataTypeCategory.TRACK: #Track Visual 부분을 Box 말고 다른 view로 바꿔봐야할 것 같음...
            box = visuals.Box(width=1, height=1, depth=1, color=(0.5, 0.5, 1, 0), edge_color='white')
            #box.transform = transforms.STTransform(translate=(0., 0., 0.), scale=(1., 1., 1.))
            matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
            mt = transforms.MatrixTransform(matrix)
            #st = transforms.STTransform(translate=(0., 0., 0.), scale=(3., 1.5, 1.))
            st = transforms.STTransform(translate=(0., 0., 0.), scale=(1., 1., 1.))
            box.transform = transforms.ChainTransform(st, mt)
            box.transform.transforms[1].scale((1.5, 1, 3))
            box.transform.transforms[1].rotate(90, (1, 0, 0))
            box.transform.transforms[1].rotate(90, (0, 0, 1))
            return box, dataview.rawid
            #return visuals.Markers(edge_color=None, size=10, symbol='square'), dataview.rawid
        else: #need to add line
            return None