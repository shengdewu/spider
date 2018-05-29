import queue
import threading
import multiprocessing

class process_task(object):

    def __init__(self, count = 4):
        self.__task_queue = queue.Queue(20)
        self.__mutx = threading.Lock()
        self.__exit = False
        self.__max_thread = count
        self.__thread = []
        for index in range(count):
            self.__thread.append(threading.Thread(target=process_task.__run__, name=index, args=(self,)))

    def __run__(self):
        while True != self.__exit:
            if True == self.__task_queue.empty():
                continue
            self.__mutx.acquire()
            task = self.__task_queue.get()
            self.__mutx.release()
            print('get :')
            print(task)
            print('\n')

    def add_task(self, args):
        self.__mutx.acquire()
        self.__task_queue.put(args)
        self.__mutx.release()
        print('put: ')
        print(args)
        print('\n')

    def stop(self):
        self.__exit = True
        for index in range(self.__max_thread):
            self.__thread[index].join()

    def start(self):
        self.__exit = False
        for index in range(self.__max_thread):
            self.__thread[index].start()



def test():
    task = process_task(count=5)
    task.start()
    while True:
        contrl = input('contrl:')
        if 'exit ' == contrl:
            break
        elif 'add' == contrl:
            args = input('agrs:')
            task.add_task(args)
    task.stop()






