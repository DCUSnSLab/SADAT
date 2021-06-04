import time

import vispy.scene
from vispy.scene import visuals
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
import numpy as np


class mainclass(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        hbox = QHBoxLayout()
        hbox.addWidget(self.canvas.native)
        self.setLayout(hbox)

        self.mytimer = QTimer()
        self.mytimer.start(100)
        self.mytimer.timeout.connect(self.draw_graph)
        self.draw_graph()
        self.setGeometry(300,100,800,500)
        self.initcanvas()
        self.show()
        vispy.app.run()
        # n = 10
        # y = np.linspace(-10, 10, n)
        # x = np.linspace(-10, 10, 100)
        # for i in range(n):
        #     yi = np.array([y[i]] * 100)
        #     d = (x ** 2 + yi ** 2) ** 0.5
        #     z = 10 * np.cos(d) / (d + 1)
        #     pts = np.vstack([x, yi, z]).transpose()
        #     # print(pts)
        #     # plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i,n*1.3)), width=(i+1)/10., antialias=True)
        #     plt = gl.GLScatterPlotItem(pos=pts, color=pg.glColor((255, 0, 0, 255)), size=1, pxMode=False)
        #     # fig1.addItem(plt)
        #     # time.sleep(0.1)

        #print(pos)

    def initcanvas(self):
        view = self.canvas.central_widget.add_view()
        grid = self.canvas.central_widget.add_grid()
        # generate data
        pos = np.random.normal(size=(10000, 3), scale=0.2)
        # one could stop here for the data generation, the rest is just to make the
        # data look more interesting. Copied over from magnify.py
        centers = np.random.normal(size=(50, 3))
        indexes = np.random.normal(size=10000, loc=centers.shape[0] / 2.,
                                   scale=centers.shape[0] / 3.)
        indexes = np.clip(indexes, 0, centers.shape[0] - 1).astype(int)
        scales = 10 ** (np.linspace(-2, 0.5, centers.shape[0]))[indexes][:, np.newaxis]
        pos *= scales
        pos += centers[indexes]

        # create scatter object and fill in the data
        scatter = visuals.Markers()
        scatter.set_data(pos, edge_color=None, face_color=(1, 1, 1, .5), size=5)

        view.add(scatter)

        view.camera = 'turntable'  # or try 'arcball'

        # add a colored 3D axis for orientation
        axis = visuals.XYZAxis(parent=view.scene)
        grid1 = visuals.GridLines(parent=view.scene)

    def draw_graph(self):
        pass



# pos = np.random.random(size=(512 * 256, 3))
# # pos *= [10, -10, 10]
# # d2 = (pos ** 2).sum(axis=1) ** 0.5
# # pos[:, 2] = d2
# color = [1, 1, 1, 1]
# size = 5
# sp = gl.GLScatterPlotItem(pos=pos, color=color, size=5, pxMode=False)
# sp.translate(-127.5, -127.5, -127.5)
# fig1.addItem(sp)

# axis = Custom3DAxis(fig1, color=(0.2,0.2,0.2,.6))
# axis.setSize(x=12, y=12, z=12)
# # Add axes labels
# axis.add_labels()
# # Add axes tick values
# axis.add_tick_values(xticks=[0,4,8,12], yticks=[0,6,12], zticks=[0,3,6,9,12])
# fig1.addItem(axis)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = mainclass()
    sys.exit(app.exec_())
    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()