#coding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree

class spider(object):
    #私有成员
    __comment_http_header = 'https://movie.douban.com/subject/'
    __comment_http_tail = '/comments?start=0&limit='

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'exc_type: '+ exc_type + ' ,exc_val:' + exc_val +', exc_tb: '+exc_tb

    def __init__(self):
        return

    def get(self, url):
        context = requests.get(url)
        context = context.content.decode('utf-8')
        return context

    def parse(self, html):
        dom_tree = etree.HTML(html);
        links = dom_tree.xpath("//div[@class='mod-bd']/ul[@class='lists']/li")
        moves = []
        for link in links:
            content = {}
            data_title = link.xpath("attribute::data-title")
            if [] == data_title:
                continue
            content['data-title'] = data_title[0]

            content['data-score'] = '#'
            value = link.xpath("attribute::data-score")
            if value:
                content['data-score']=value[0]

            content['data-star'] = '#'
            value = link.xpath("attribute::data-star")
            if value:
                content['data-star']=value[0]

            content['data-region'] = '#'
            value = link.xpath("attribute::data-region")
            if value:
                content['data-region']=value[0]

            content['data-subject'] = '#'
            value = link.xpath("attribute::data-subject")
            if value:
                content['data-subject']=value[0]

            moves.append(content)
        return moves

    def get_comment(self, data_subject, limit):
        http = self.__comment_http_header + data_subject + self.__comment_http_tail + str(limit)
        html = self.get(http)

        dom_tree = etree.HTML(html)
        links = dom_tree.xpath("//div[@class='comment']/p[@class]")
        comment = []
        for link in links:
            value = link.xpath("child::text()")
            if value:
                comment.append(value[0])
        return comment