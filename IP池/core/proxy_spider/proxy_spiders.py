from core.proxy_spider.base_spider import BaseSpider


# 西刺代理
class XiCiSpider(BaseSpider):
    urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'
    }


# IP3366代理
class Ip3366Spider(BaseSpider):
    urls = ['http://www.ip3366.net/?stype=1&page={}'.format(i) for i in range(1, 7)]
    # 分组的xpath
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


# 快代理
class KuaiSpider(BaseSpider):
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 7)]
    # 分组的xpath
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


# 66ip
class Ip66Spider(BaseSpider):
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }


if __name__ == '__main__':
    spider = XiCiSpider()
    for proxy in spider.get_proxies():
        print(proxy)

