import requests
from utils.http import get_request_headers
from lxml import etree
from donmain import Proxy


class BaseSpider(object):
    # 代理IP网址的url的列表
    urls = []
    # 分组XPATH， 获取包含代理IP信息标签列表的XPATH
    group_xpath = ''
    # 获取代理IP详情的信息XPATH，格式为: {'ip':'xx', 'port':'xx", 'area':'xx'}
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath="", detail_xpath={}):
        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content

    def get_first_from_list(self, lis):
        # 如果列表中有元素，就返回第一个， 否则就返回空字符串
        return lis[0] if len(lis) != 0 else ''

    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        # 获取包含代理IP信息的标签列表
        trs = element.xpath(self.group_xpath)
        # 遍历trs，获取代理IP相关信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            # 使用yield返回提取到的数据
            yield proxy

    def get_proxies(self):
        for url in self.urls:
            # 根据发送请求，获取页面数据
            page = self.get_page_from_url(url)
            # 解析页面，提取数据，封装Proxy对象
            proxies = self.get_proxies_from_page(page)
            # 返回Proxy对象列表
            yield from proxies


