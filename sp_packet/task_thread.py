from multiprocessing import Process,Queue,Pool
from sp_packet import spider
from sp_packet import parse
import os

class task_thread(Process):
    def __init__(self, url, queue):
        super(task_thread, self).__init__()
        self.__queue = queue
        self.__url = url
        return

    def run(self):
        print "moduel name " + __name__ + ", pid " + str(os.getpid())

        s = spider.spider()

        content = s.get(self.__url)
        moves = s.parse(content)
        print moves

        p = parse.parse()
        comments = p.get_comment(moves)
        print comments

        self.__queue.put(comments);
        for (key, value) in comments.items():
            p.parse_word(key, value)
        return

