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
    return [r, g, b, 1]

b = np.load('pdata.npy')

start = time.time()
for i in range(100):
    res = np.apply_along_axis(num_to_rgb,1,b)
print(time.time()-start)

start = time.time()
for i in range(100):
    color = [num_to_rgb2(b[i][3]) for i in range(len(b))]
print(time.time()-start)