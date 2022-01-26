# pyline: disable=no-member
""" plot3d using existing visuals : LinePlotVisual """

import numpy as np
import sys

from vispy import app, visuals, scene

# build visuals
Plot3D = scene.visuals.create_visual_node(visuals.LinePlotVisual)

# build canvas
canvas = scene.SceneCanvas(keys='interactive', title='plot3d', show=True)

# Add a ViewBox to let the user zoom/rotate
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.fov = 45
view.camera.distance = 6

mdata = 1
icd = 1
# prepare data
N = 60
# x = np.sin(np.linspace(-2, 2, N)*np.pi)
# y = np.cos(np.linspace(-2, 2, N)*np.pi)
# z = np.linspace(-2, 2, N)
x = np.array([0, 10, 10, 0, 0])
y = np.array([0, 0, 10, 10, 0])
z = np.array([0, 0, 0, 0, 0])

# plot
pos = np.c_[x, y, z]
p3d = Plot3D(pos, width=2.0, color='red',
       edge_color='w', face_color=(0.2, 0.2, 1, 0.8),
       parent=view.scene)

def update(event):
    global mdata, icd, x, y, z
    if mdata == 50 or mdata == 0:
        icd *= -1
    mdata += icd
    x += icd
    p3d.set
    print(mdata)

timer = app.Timer('auto', connect=update, start=True)

# class LineCube():
#     def __init__(self, size=None):
#         if size is None:
#             self.size = np.array([0, 0, 0]) #width, height, depth




if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()
