from sp_packet import spider
from sp_packet import parse
from sp_packet import task_thread
from multiprocessing import Queue
from sp_packet import dynamic_spider

def excute():
    url = 'https://user.qzone.qq.com/446868355'
    url = 'https://movie.douban.com/nowplaying/hangzhou/'
    s = spider.spider()

    # content = s.get(url)
    # moves = s.parse(content)
    # print(moves)
    #
    # p = parse.parse()
    # comments = p.get_comment(moves)
    # print(comments)

    # for (key, value) in comments.items():
    #     p.parse_word(key, value)

    url_list = ['https://movie.douban.com/cinema/nowplaying/chengdu/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/',
                'https://movie.douban.com/nowplaying/hangzhou/']

    queue = Queue()
    process = []
    for url in url_list:
        task = task_thread.task_thread(url, queue)
        process.append(task)
        task.start()

    for p in process:
        p.join()

    print("process is finish##########################")
    while not queue.empty():
        print(queue.get())

    return

if __name__ == '__main__':
    dynamic_spider.test()

