"""step 1 导入依赖库"""
from os import path
from browsermobproxy import Server
from selenium import webdriver
import re
"""step 2 新建浏览器监控类"""


class Monitor(object):
    """
    step 3 配置chromedriver 和 browermobproxy 路径
    需要使用完整路径，否则browsermobproxy无法启动服务
    我是将这两个部分放到了和monitor.py同一目录
    同时设置chrome为屏蔽图片，若需要抓取图片可自行修改
    """
    PROXY_PATH = path.abspath("./browsermob-proxy-2.1.4/bin/browsermob-proxy.bat")
    CHROME_PATH = path.abspath("./web_driver/geckodriver.exe")
    CHROME_OPTIONS = {"profile.managed_default_content_settings.images": 2}

    def __init__(self):
        """
        类初始化函数暂不做操作
        """
        pass

    def initProxy(self):
        """
        step 4 初始化 browermobproxy
        设置需要屏蔽的网络连接，此处屏蔽了css，和图片（有时chrome的设置会失效），可加快网页加载速度
        新建proxy代理地址
        """
        self.server = Server(self.PROXY_PATH)
        self.server.start()
        self.proxy = self.server.create_proxy()
        self.proxy.blacklist(["http://.*/.*.css.*", "http://.*/.*.jpg.*", "http://.*/.*.png.*", "http://.*/.*.gif.*"],
                             200)

    def initChrome(self):
        """
        step 5 初始化selenium， chrome设置
        将chrome的代理设置为browermobproxy新建的代理地址
        """
        profile = webdriver.FirefoxProfile()
        profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=self.CHROME_PATH)


    def genNewRecord(self, name="monitor", options={'captureContent': True}):
        """
        step 6 新建监控记录，设置内容监控为True
        """
        self.proxy.new_har(name, options=options)

    def getContentText(self, targetUrl):
        """
        step 7 简单的获取目标数据的函数
        其中 targetUrl 为浏览器获取对应数据调用的url，需要用正则表达式表示
        """
        self.proxy.wait_for_traffic_to_stop(1, 60)

        return self.proxy.har

        # if self.proxy.har['log']['entries']:
        #     for loop_record in self.proxy.har['log']['entries']:
        #         try:
        #             if re.fullmatch(targetUrl, loop_record["request"]['url']):
        #                 return loop_record["response"]['content']["text"]
        #         except Exception as err:
        #             print(err)
        #             continue
        # return None

    def Start(self):
        """step 8 配置monitor的启动顺序"""
        try:
            self.initProxy()
            self.initChrome()
        except Exception as err:
            print(err)

    def Quit(self):
        """
        step 9 配置monitor的退出顺序
        代理sever的退出可能失败，目前是手动关闭，若谁能提供解决方法，将不胜感激
        """
        self.driver.close()
        self.driver.quit()
        try:
            self.proxy.close()
            self.server.process.terminate()
            self.server.process.wait()
            self.server.process.kill()
        except OSError:
            pass

#实验成功,推荐是使用firefox
def test_browser():
    PROXY_PATH = path.abspath("./browsermob-proxy-2.1.4/bin/browsermob-proxy.bat")
    FIREFOX_PATH = path.abspath("./web_driver/geckodriver.exe")

    server = Server(PROXY_PATH)
    server.start()
    proxy = server.create_proxy()

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=FIREFOX_PATH)

    proxy.new_har("baidu")
    driver.get("https://s.taobao.com/search?q=薯条")
    proxy.wait_for_traffic_to_stop(1, 60)
    # with open('1.har', 'w') as outfile:
    #     json.dump(proxy.har, outfile)
    print(proxy.har)
    server.stop()
    driver.quit()

#实验失败,推荐是使用firefox
def test():

    monitor = Monitor()
    monitor.Start()
    monitor.genNewRecord()

    monitor.driver.get("https://s.taobao.com/search?q=薯条")
    targetUrl = "https://s.taobao.com/api.*?"
    text = monitor.getContentText(targetUrl)

    print(text)
    monitor.Quit()

    return