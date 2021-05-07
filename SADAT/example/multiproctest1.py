import multiprocessing as mp
import ctypes
from ctypes import Structure

from time import sleep

import ctypes
BUFSIZE = 1024

class my_struct(ctypes.Structure):
    _fields_ = [ ("name", ctypes.c_double),
                 ("size", ctypes.c_int )]


def worker(mq, a):
    print('Start Worker')
    print('wait queue')
    while True:
        cnt = 1
        for data in mq:
            print('worker',cnt,'->',data.name, id(data))
            cnt += 1

        sleep(1)

if __name__ == "__main__":

    arr = mp.Array(my_struct, 2)
    a = 1
    p = mp.Process(name="SubProcess", target=worker, args=[arr, a])
    p.start()
    sleep(1)
    arr[0].name = 2.0
    sleep(1)
    p.terminate()
    #print('origin->',temp1.id, id(temp1))
    #sleep(1)
    #print('origin->', temp1.id, id(temp1))

