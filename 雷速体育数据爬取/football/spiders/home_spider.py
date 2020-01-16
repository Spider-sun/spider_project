from gevent import monkey
monkey.patch_all()

import requests
import re
import time
import schedule

from lxml import etree
from gevent.pool import Pool
from queue import Queue

from football.db.mongo_pool import MongoDB
from football.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from football.settings import HEADERS, TEST_HOME_ASYNC_COUNT


class HomePage(object):
    def __init__(self, name):
        self.name = name
        # 建立数据库连接
        self.mongo = MongoDB('football_home_page')
        self.redis = Redis_Pool()
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        '''异步回调函数'''
        if not self.queue.empty():
            self.coroutine_pool.apply_async(self.__dispose_one_data, callback=self.__chech_callbake)

    def get_data(self):
        live = self.redis.find(self.name)
        threads = []
        for k, v in live.items():
            # self.__dispose_one_data(events, li, teams)
            msg = eval(v.decode("utf-8"))
            self.queue.put(msg)

        for i in range(TEST_HOME_ASYNC_COUNT):
            if not self.queue.empty():
                self.coroutine_pool.apply_async(self.__dispose_one_data, callback=self.__chech_callbake)
                # time.sleep(2)
            # 守护线程
        self.coroutine_pool.join()

    def __dispose_one_data(self):
        proxy = get_ip()
        if not self.queue.empty():
            msg = self.queue.get()
            try:
                if proxy:
                    response = requests.get('https://live.leisu.com/detail-' + str(msg['赛事ID']), proxies={'https': 'https://'+proxy}, headers=HEADERS, allow_redirects=False).text
                else:
                    response = requests.get('https://live.leisu.com/detail-' + str(msg['赛事ID']), headers=HEADERS, allow_redirects=False).text
                # print(response)
                # 文字解说
                narrate_ = re.findall('EVENT=(.*?])', response)
                if narrate_:
                    narrate = narrate_[0].replace('雷速体育', '我们')
                else:
                    narrate = ''
                html = etree.HTML(response)
                # 比分
                try:
                    score = f'''{html.xpath('//div[@class="score home"]/text()')[0]}-{html.xpath('//div[@class="score away"]/text()')[0]}'''
                except:
                    score = ''
                # 半场
                half_score_ = html.xpath('//span[@class ="half-score"]/text()')
                if half_score_:
                    half_score = half_score_[0]
                else:
                    half_score = ''
                # 角球
                lab_data = html.xpath('//span[@class="lab corner"]/span[@class="text"]/text()')
                if lab_data:
                    lab_corner = lab_data[0] + '-' + lab_data[1]
                else:
                    lab_corner = ''

                msg['半场'] = half_score
                msg['角球'] = lab_corner
                msg['解说'] = narrate
                self.mongo.insert_one(msg, '赛事ID')
            except requests.exceptions.ProxyError:
                pass

    @classmethod
    def start(cls):
        def run():
            notStart = cls('football_notStart')
            finished = cls('football_finished')
            other = cls('football_other')
            live = cls('football_live')
            live.get_data()
            notStart.get_data()
            finished.get_data()
            other.get_data()

        run()
        # 每隔一段时间执行一次run方法
        schedule.every(2).seconds.do(run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    HomePage.start()