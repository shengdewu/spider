from sp_packet import spider
from sp_packet import parse

def excute():
    url = 'https://user.qzone.qq.com/446868355'
    url = 'https://movie.douban.com/nowplaying/hangzhou/'
    s = spider.spider()

    content = s.get(url)
    moves = s.parse(content)
    print moves

    p = parse.parse()
    comments = p.get_comment(moves)
    print comments

    for (key, value) in comments.items():
        p.parse_word(key, value)

excute()

