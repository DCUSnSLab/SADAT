import random

import vispy.scene
from vispy.scene import visuals, TurntableCamera
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtGui
import numpy as np
from vispy.visuals.transforms import MatrixTransform
from vispy.visuals import transforms

from dadatype.dtype_cate import DataTypeCategory


class planView3D(QWidget):
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
        self.view.camera = TurntableCamera(fov=30.0, elevation=90.0, azimuth=-90., distance=100, translate_speed=50.0)
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
            if pos[1] == 0 and pos[0] == 0:
                viewitem.set_data([0., 0., 0.], width=0)
            else:
                viewitem.set_data(pos)
        elif dataview.viewType == DataTypeCategory.LINE:
            pass
        elif dataview.viewType == DataTypeCategory.LANE:
            pass

    def __drawInvisible(self, viewitem, dataview, pos, size, color):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            viewitem.set_data(pos=np.array([[0,0,0]]),size=0)
        elif dataview.viewType == DataTypeCategory.TRACK:
            viewitem.set_data(pos=pos, width=0)

        elif dataview.viewType == DataTypeCategory.LINE:
            pass
        elif dataview.viewType == DataTypeCategory.LANE:
            pass

    def updateItems(self, key, values):
        if (key in self.itemlist) is False:
            self.itemlist[key] = dict()
            il = self.itemlist[key]
            for i, item in enumerate(values):
                it, id, isCustom = self.applyGLObject(item)
                il[id] = it
                if isCustom is False:
                    self.view.add(it)
                else:
                    self.view.add(it.getVisual())

            #set Visible Mode Changer
            self.isOnceExeInvMode[key] = False

    # Return Type
    # Visual Object, raw id, Is custom Object
    def applyGLObject(self, dataview):
        if dataview.viewType == DataTypeCategory.POINT_CLOUD:
            return visuals.Markers(edge_color=None, size=2), dataview.rawid, False
        elif dataview.viewType == DataTypeCategory.TRACK: #Track Visual 부분을 Box 말고 다른 view로 바꿔봐야할 것 같음...
            box = sCube()
            return box, dataview.rawid, True
        else: #need to add line
            return None

class sCube():
    def __init__(self, parent=None, pos=None):
        self.isWidthZero = False
        if pos is None:
            pos = [0., 0., 0.]
        else:
            pos

        x = 0.5
        y = 0.5
        z = 0.5
        v = np.array([[x, y, z], [-x, y, z], [-x, -y, z], [x, -y, z],
                      [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, -z]])

        self.Vertice = np.array([v[0], v[1],
                              v[2], v[3],
                              v[0], v[3],
                              v[4], v[5],
                              v[0], v[5],
                              v[6], v[1],
                              v[1], v[6],
                              v[7], v[2],
                              v[7], v[4]], dtype=np.float64)

        #print(self.Vertice)
        self.accAxis = [0., 0., 0.]

        V = self.calcPos(pos)

        self.lplot = visuals.LinePlot(V, width=2.0, color='red',
                                   edge_color='w', face_color=(0.2, 0.2, 1, 0.8),
                                   parent=parent)

    def calcPos(self, pos):
        self.Vertice[:, :] -= self.accAxis
        self.Vertice[:, :] += pos
        self.accAxis = pos
        return self.Vertice


    def set_data(self, pos, width=2):
        if type(pos).__module__ == np.__name__:
            ldata = pos.tolist()
        else:
            ldata = pos
        V = self.calcPos(ldata)

        if width == 0 and self.isWidthZero is False:
            self.isWidthZero = True
            self.lplot.set_data(V, width=0)
        elif width != 0:
            self.isWidthZero = False
            self.lplot.set_data(V, width=width)

    def getVisual(self):
        return self.lplot