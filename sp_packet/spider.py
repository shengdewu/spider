#coding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree

class spider(object):
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
        # links = dom_tree.xpath("//div[@id='nowplaying']");
        #
        # moves = {}
        # for link in links:
        #     items = link.xpath("//ul[@class='lists']")
        #     for item in items:
        #         value = item.xpath("//li[@data-title]");
        #         print value

        #'//div[@id="content_right"]/div[@class="content_list"]/ul/li[div]'

        #links = dom_tree.xpath("//div[@id='nowplaying']//ul[@class='lists']/li[@data-title]");

        links = dom_tree.xpath("//div[@class='mod-bd']/ul[@class='lists']/li")
        moves = {}
        for link in links:
            value = link.xpath("attribute::data-title")[0]
            print value


        return links