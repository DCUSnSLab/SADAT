import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        #self.view.setRange(QtCore.QRectF(0,0, 100, 100))

        #  image plot
        self.img = pg.ImageItem(border='w')
        #self.view.addItem(self.img)

        self.canvas.nextRow()
        #  line plot
        #self.otherplot = self.canvas.addPlot()
        #self.h2 = self.otherplot.plot(pen='y')
        #self.h2 = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='r'), symbol='o', size=1)
        self.h2 = pg.ScatterPlotItem(symbol='o', size=1)
        self.view.addItem(self.h2)
        #### Set Data  #####################

        self.x = np.linspace(0,50., num=100)
        self.X,self.Y = np.meshgrid(self.x,self.x)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):

        self.data = np.sin(self.X/3.+self.counter/9.)*np.cos(self.Y/3.+self.counter/9.)
        self.ydata = np.sin(self.x/3.+ self.counter/9.)

        self.img.setImage(self.data)

        #Generate random points
        n = 10000
        #print('Number of points: ' + str(n))
        data = np.random.normal(size=(2, n))
        pos = [{'pos': data[:, i]} for i in range(n)]
        x = np.random.normal(size=n)
        y = np.random.normal(size=n)
        z = np.random.normal(size=n)

        cm = pg.colormap.get('jet', source='matplotlib')
        pen = cm.getPen(span=(np.min(z), np.max(z)))
        self.h2.setData(x=x,y=y)
        self.h2.setPen(pen)

        #self.h2.setData(self.ydata)

        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        QtCore.QTimer.singleShot(20, self._update)
        self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())