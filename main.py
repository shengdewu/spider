from sp_packet import spider

def excute():
    url = 'https://user.qzone.qq.com/446868355'
    url = 'https://movie.douban.com/nowplaying/hangzhou/'
    s = spider.spider()

    content = s.get(url)

    print content

    lable = s.parse(content)


excute()

