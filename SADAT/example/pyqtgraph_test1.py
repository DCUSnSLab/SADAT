import time

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import OpenGL.GL as ogl
import numpy as np


class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, X, Y, Z, text):
        gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def setText(self, text):
        self.text = text
        self.update()

    def setX(self, X):
        self.X = X
        self.update()

    def setY(self, Y):
        self.Y = Y
        self.update()

    def setZ(self, Z):
        self.Z = Z
        self.update()

    def paint(self):
        self.GLViewWidget.qglColor(QtCore.Qt.black)
        self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


class Custom3DAxis(gl.GLAxisItem):
    """Class defined to extend 'gl.GLAxisItem'."""
    def __init__(self, parent, color=(0,0,0,.6)):
        gl.GLAxisItem.__init__(self)
        self.parent = parent
        self.c = color

    def add_labels(self):
        """Adds axes labels."""
        x,y,z = self.size()
        #X label
        self.xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
        self.xLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabel)
        #Y label
        self.yLabel = CustomTextItem(X=-x/20, Y=y/2, Z=-z/20, text="Y")
        self.yLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabel)
        #Z label
        self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z/2, text="Z")
        self.zLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabel)

    def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
        """Adds ticks values."""
        x,y,z = self.size()
        xtpos = np.linspace(0, x, len(xticks))
        ytpos = np.linspace(0, y, len(yticks))
        ztpos = np.linspace(0, z, len(zticks))
        #X label
        for i, xt in enumerate(xticks):
            val = CustomTextItem(X=xtpos[i], Y=-y/20, Z=-z/20, text=str(xt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Y label
        for i, yt in enumerate(yticks):
            val = CustomTextItem(X=-x/20, Y=ytpos[i], Z=-z/20, text=str(yt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Z label
        for i, zt in enumerate(zticks):
            val = CustomTextItem(X=-x/20, Y=-y/20, Z=ztpos[i], text=str(zt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            ogl.glEnable(ogl.GL_LINE_SMOOTH)
            ogl.glHint(ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST)
        ogl.glBegin(ogl.GL_LINES)

        x,y,z = self.size()
        #Draw Z
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, 0, z)
        #Draw Y
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, y, 0)
        #Draw X
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(x, 0, 0)
        ogl.glEnd()

class mainclass(QWidget):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout()
        self.fig1 = gl.GLViewWidget()
        #self.background_color = self.app.palette().color(QtGui.QPalette.Background)
        self.fig1.setBackgroundColor((0, 0, 0))
        self.fig1.opts['distance'] = 100
        hbox.addWidget(self.fig1)
        self.setLayout(hbox)

        self.mytimer = QTimer()
        self.mytimer.start(100)
        self.mytimer.timeout.connect(self.draw_graph)
        self.draw_graph()
        self.setGeometry(300,100,800,500)
        self.show()
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
    @pyqtSlot()
    def draw_graph(self):
        self.fig1.clear()
        pts = [[1.0, 1.0, 0.0], [10.0, 10.0, 10.0], [1000, 10, 10]]
        pts = np.random.random(size=(3, 3))
        pts *= [10, -10, 0]
        color = [pg.glColor((255, 0, 0, 255)), pg.glColor((0, 255, 0, 255)), pg.glColor((0, 0, 255, 255))]
        pts = np.array(pts)
        color = np.array(color)
        #print(pts)
        #print(color)
        gv = gl.GLGridItem()
        gv.setSize(100,100,100)
        self.fig1.addItem(gv)
        plt = gl.GLScatterPlotItem(pos=pts, color=color, size=0.1, pxMode=False)
        self.fig1.addItem(plt)



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