#coding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree
import random

import re

class spider(object):
    #私有成员
    __comment_http_header = 'https://movie.douban.com/subject/'
    __comment_http_tail = '/comments?start=0&limit='

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exc_type: '+ exc_type + ' ,exc_val:' + exc_val +', exc_tb: '+exc_tb)

    def __init__(self):
        return

    def get(self, url):
        try:
            header = {
                # 'Host': "www.xicidaili.com",  # 需要修改
                # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                # "Accept-Encoding": "gzip, deflate",
                # "Accept-Language": "en-US,en;q=0.5",
                # "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0\\r\\"
            }
            proxy_ip = ['172.16.6.15', '172.16.6.16', '172.16.6.17', '172.16.6.18', '172.16.6.19', '172.16.6.20']
            ip = {'http': random.choice(proxy_ip)}
            context = requests.get(url, proxies=ip,headers=header)
            context = context.content.decode('utf-8')
            return context
        except requests.HTTPError as code:
            print("request is failed:" + str(code))
        except requests.ConnectionError as code:
            print("request is failed:" + str(code))
        return


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
        comment = ''
        for link in links:
            value = link.xpath("child::text()")
            if value:
                #value = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf-8"), "".decode("utf-8"),value[0])
                comment += value[0]
        return comment