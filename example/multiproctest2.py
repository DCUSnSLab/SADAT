from multiprocessing import Process, Semaphore, shared_memory
import numpy as np
import time

import rospy
from sensor_msgs.msg import PointCloud2, CompressedImage


def worker(id, number, a, shm, serm):
    print(id, 'worker sub - ',a)
    rname = 'listner'+str(id)
    rospy.init_node(rname, anonymous=True)
    rospy.Subscriber(a, number, shm)
    rospy.spin()

def callback(msg):
    data = msg
    print(data._type)

def callbackcam(msg):
    data = msg
    print(data._type)

if __name__ == "__main__":
    serm = Semaphore(1)
    start_time = time.time()

    a = np.array([0])
    shm = shared_memory.SharedMemory(
        create=True, size=a.nbytes)  # 공유 메모리 블록 생성
    # 공유 메모리에 NumPy 배열을 만든다 > 프로세스에서 만든 NumPy 배열의 변경을 반영
    c = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    th1 = Process(target=worker, args=(1, PointCloud2, "/velodyne_points", callback, serm))
    th2 = Process(target=worker, args=(2, CompressedImage, "/usb_cam/image_raw/compressed", callbackcam, serm))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("total_number=", end=""), print(c[0])
    shm.close()
    shm.unlink()
    print("end of main")