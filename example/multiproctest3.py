from time import sleep

from multiprocessing import Process
import numpy as np

from utils.arrayqueues.shared_arrays import ArrayQueue


class ReadProcess(Process):
    def __init__(self, source_queue, id):
        super().__init__()
        self.idd = id
        self.source_queue = source_queue

    def run(self):
        print('tested', self.idd)
        while True:
            data = self.source_queue.get()
            sleep(0.05)
        #print(self.idd, '-', data, id(data))


if __name__ == "__main__":
    q1 = ArrayQueue(3000)  # intitialises an ArrayQueue which can hold 1MB of data
    r = ReadProcess(q1, 1)
    r.start()
    #r2 = ReadProcess(q2, 2)
    #r2.start()
    a = 1
    n = np.full((1920, 1080), 1)
    print(n.size)
    print('origin id',id(n), n)
    for i in range(1000):
        q1.put(n)
        print(q1.qsize())
        sleep(0.033)
    r.join()

