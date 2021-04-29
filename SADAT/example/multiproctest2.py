from multiprocessing import Process, Semaphore, shared_memory
import numpy as np
import time


def worker(id, number, a, shm, serm):
    num = 0
    for i in range(number):
        num += 1

    serm.acquire()  # 세마포어로 공유 메모리에 프로세스 한 개만 접근하도록 제한
    exst_shm = shared_memory.SharedMemory(name=shm)  # 공유 메모리에 연결

    b = np.ndarray(a.shape, dtype=a.dtype, buffer=exst_shm.buf)  # 공유 메모리에 배열 생성
    b[0] += num  # 최종 결과를 배열에 저장

    serm.release()


if __name__ == "__main__":
    serm = Semaphore(1)
    start_time = time.time()

    a = np.array([0])
    shm = shared_memory.SharedMemory(
        create=True, size=a.nbytes)  # 공유 메모리 블록 생성
    # 공유 메모리에 NumPy 배열을 만든다 > 프로세스에서 만든 NumPy 배열의 변경을 반영
    c = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    th1 = Process(target=worker, args=(1, 50000000, a, shm.name, serm))
    th2 = Process(target=worker, args=(2, 50000000, a, shm.name, serm))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("total_number=", end=""), print(c[0])
    shm.close()
    shm.unlink()
    print("end of main")