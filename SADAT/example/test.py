import math
import numpy as np
import time

def num_to_rgb( val, max_val=255):
    i = (val[3] * 255 / max_val);
    r = round(math.sin(0.024 * i + 0) * 127 + 128);
    g = round(math.sin(0.024 * i + 2) * 127 + 128);
    b = round(math.sin(0.024 * i + 4) * 127 + 128);
    return [r, g, b, 1]

def num_to_rgb2( val, max_val=255):
    i = (val * 255 / max_val);
    r = math.sin(0.024 * i + 0) * 127 + 128
    g = math.sin(0.024 * i + 2) * 127 + 128
    b = math.sin(0.024 * i + 4) * 127 + 128
    return [r/255, g/255, b/255, 1]

b = np.load('pdata.npy')
res = 1
maxval = 141
cnt = maxval * res
color = [i*(1/res) for i in range(cnt)]
print(color)
cmap = [num_to_rgb2(color[i]) for i in range(len(color))]
cmap = np.array(cmap)
print(cmap)
# points = np.zeros((b.shape[0], 7))
# color = [num_to_rgb2(b[i][3]) for i in range(len(b))]
# color = np.array(color)
# data = color[:, 0]
# points[:,3:7] = color[:,0:4]
# discolor = points[:, 3:7]
# print(points)
result = np.zeros((b.shape[0], 4))
start = time.time()
#for i in range(100):
inten = b[:,3].astype(np.int32)
result = np.array([cmap[inten[i]] for i in range(len(b))])
print(time.time()-start)

start = time.time()
#for i in range(100):
result = np.apply_along_axis(num_to_rgb,1,b)
print(time.time()-start)
#
start = time.time()
#for i in range(100):
color = [num_to_rgb2(b[i][3]) for i in range(len(b))]
print(time.time()-start)