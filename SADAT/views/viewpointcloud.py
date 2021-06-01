import math

from pyqtgraph.opengl import GLScatterPlotItem

from views.DataView import DataView
import pyqtgraph as pg
import numpy as np

class viewPointCloud(DataView):
    def __init__(self, pdata=None):
        super().__init__(rawdata=pdata)
        self.colorrange = list()
        self.setColorRange()

    def PlanViewPos(self):
        self.pvpos=self.updatePlanviewPos()


    def setColorRange(self):
        a = np.array(pg.glColor((255,0,0,255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((255, 0, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((255, 101, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((255, 179, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((255, 244, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((215, 244, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((79, 244, 0, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 255, 128, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 255, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)
        a = np.array(pg.glColor((0, 0, 255, 255)))
        self.colorrange.append(a)

    def drawIndividual(self,qp,xp,yp,ikey):
        qp.drawEllipse(xp,yp,6,6)

    def num_to_rgb(self, val, max_val=141):
        i = (val * 255 / max_val);
        r = math.sin(0.024 * i + 0) * 127 + 128
        g = math.sin(0.024 * i + 2) * 127 + 128
        b = math.sin(0.024 * i + 4) * 127 + 128
        return [r/255, g/255, b/255, 1]

    def draw3DVisual(self, pos, ikey):
        #np.save('pdata', pos)
        #print(pos[0])
        color = [self.num_to_rgb(pos[i][3]) for i in range(len(pos))]
        #color = np.zeros((pos.shape[0], 4))
        #color[:] = [1,1,1,1]

        #color = np.apply_along_axis(self.num_to_rgb, 1, pos)

        #color = np.array(color, dtype=np.float32)
        #print(type(pos), len(pos))
        # npos = list()
        # cpos = list()
        # for i in range(0, 20, 1):
        #     npos.append(pos + [0, 0, i])
        #     cpos.append(color + self.colorrange[i])
        # pos = np.vstack(npos)
        # color = np.vstack(cpos)
        #print(pos.dtype, color.dtype)

        return pos, color
        #self.globject.setData(pos=pos, color=color, size=0.5, pxMode=False)
        #print(pos)
        #plt = gl.GLScatterPlotItem(pos=pos, color=color, size=0.5, pxMode=False)
