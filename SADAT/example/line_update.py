# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Demonstration of animated Line visual.
"""

import sys
import numpy as np
from vispy import app, scene
#vertex positions of data to draw
from vispy.scene import visuals, TurntableCamera
from vispy.visuals import Visual

def meth1(pts):
   pts = np.array(pts)  #Skip if pts is a numpy array already
   lp = len(pts)
   arr = np.zeros((lp,lp,lp,3))
   arr[:,:,:,0] = pts[:,None,None]  #None is the same as np.newaxis
   arr[:,:,:,1] = pts[None,:,None]
   arr[:,:,:,2] = pts[None,None,:]
   return arr

N = 200

# color array
color = np.ones((N, 4), dtype=np.float32)
color[:, 0] = np.linspace(0, 1, N)
color[:, 1] = color[::-1, 0]

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'arcball'
grid1 = visuals.GridLines(parent=view.scene)
axis = visuals.XYZAxis(parent=view.scene)
view.camera = TurntableCamera(fov=30.0, elevation=90.0, azimuth=0., distance=100, translate_speed=50.0)
view.camera.fov = 45
view.camera.distance = 6

class sCube():
    def __init__(self, parent=None, pos=None):
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

        self.accAxis = [0., 0., 0.]

        V = self.calcPos(pos)

        self.lplot = visuals.LinePlot(V, width=2.0, color='red',
                                   edge_color='w', face_color=(0.2, 0.2, 1, 0.8))

    def calcPos(self, pos):
        self.Vertice[:, :] -= self.accAxis
        self.Vertice[:, :] += pos
        self.accAxis = pos
        return self.Vertice

    def set_data(self, pos, width=2):
        ldata = None
        if type(pos).__module__ == np.__name__:
            ldata = pos.tolist()
        else:
            ldata = pos
        V = self.calcPos(ldata)
        self.lplot.set_data(V, width=width)

    def getVisual(self):
        return self.lplot

mdata = 1.
icd = 0.1
'''
v = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
         [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]
 '''
# v = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
#          [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]])
#
# V = np.array([v[0], v[1],
#               v[2], v[3],
#               v[0], v[3],
#               v[4], v[5],
#               v[0], v[5],
#               v[6], v[1],
#               v[1], v[6],
#               v[7], v[2],
#               v[7], v[4]])


# viewbox = grid.add_view(row=0, col=1, camera='panzoom')
#
# # add some axes
# x_axis = scene.AxisWidget(orientation='bottom')
# x_axis.stretch = (1, 0.1)
# grid.add_widget(x_axis, row=1, col=1)
# x_axis.link_view(viewbox)
# y_axis = scene.AxisWidget(orientation='left')
# y_axis.stretch = (0.1, 1)
# grid.add_widget(y_axis, row=0, col=0)
# y_axis.link_view(viewbox)

# add a line plot inside the viewbox
#line = scene.Line(pos, color, parent=view.scene)
#pos = np.c_[x, y, z]
aa = np.array([1., 0., 0.])
p3d = sCube(pos=aa)
aa = [0., 0., 0.]
print(type(aa))
#p3d2 = sCube(pos=aa)
view.add(p3d.getVisual())
#view.add(p3d2.getVisual())
#p3d.set_data(pos=[2., 0., 0.])
#p3d = visuals.Line(pos, width=1.0, parent=view.scene)

# auto-scale to see the whole line.
#viewbox.camera.set_range()



def update(ev):
    global mdata, icd, p3d
    if int(mdata) == 10 or int(mdata) == 0:
        icd *= -1
    mdata += icd
    #print(mdata)

    # x += icd
    # #p3d.set
    # x += icd
    # print(mdata)
    # pos = np.c_[x, y, z]
    p3d.set_data([0., 0., 0.], width=0)

timer = app.Timer()
timer.connect(update)
timer.start(0)

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
