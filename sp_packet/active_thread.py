import multiprocessing
import queue
import threading

task_cnt = 0

class active_thread(object):

    def __init__(self, max_thead = 4, max_queue_size = 10):
        self.__exit = False
        self.__queue = queue.Queue(max_queue_size)
        self.__queue_mtx = threading.Lock()
        self.__thread = []
        self.__wait_mtx = threading.Lock()
        self.__condition = threading.Event()
        for cnt in range(max_thead):
            self.__thread.append(threading.Thread(target = active_thread.__run__, name = cnt, args=(self,)))
        return

    def __run__(self):
        while True != self.__exit:
            if True == self.__queue.empty():
                self.__condition.wait()
                continue
            self.__queue_mtx.acquire()
            task = self.__queue.get()
            self.__queue_mtx.release()
            task[0](*task[1])
        print('exit....')


    def add_task(self, *args):
        if self.__queue.full():
            return False
        self.__queue_mtx.acquire()
        self.__queue.put(args)
        self.__queue_mtx.release()
        self.__condition.set()
        print('put: task')
        return True

    def stop(self):
        self.__exit = True
        for index in range(len(self.__thread)):
            self.__thread[index].join()

    def start(self):
        self.__exit = False
        for index in range(len(self.__thread)):
            self.__thread[index].start()


class tfunc():
    def pint_name(self, args=()):
            print(args)

def test():

    test_task = active_thread(max_thead = 5, max_queue_size=100)

    test_task.start()


    for i in range(100):
        tf = tfunc()
        args = [tfunc.pint_name, [tf, ('my', 'is', str(i))]]
        print(test_task.add_task(*args))
        print(i)

    input('wait:\n')

    test_task.stop()