from PyQt5.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np


class planView(QWidget):
    def __init__(self, planviewmanager):
        super().__init__()
        self.cnt = 0
        #set planview manager
        self.pvmanager = planviewmanager

        hbox = QHBoxLayout()
        self.glwidget = gl.GLViewWidget()
        self.glwidget.setBackgroundColor((0,0,0))
        self.glwidget.opts['distance'] = 100
        hbox.addWidget(self.glwidget)
        self.setLayout(hbox)
        self.draw()

    def draw(self):
        print('draw planview',self.cnt)
        self.cnt+=1
        for ikey, values in self.pvmanager.getObjects():
            for idata in values:
                # if self.combo.item_checked(index=0):
                #         idata.setVisible(True)
                item = idata.draw(ikey, gl)
                if item is not None:
                    self.glwidget.addItem(item)

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
