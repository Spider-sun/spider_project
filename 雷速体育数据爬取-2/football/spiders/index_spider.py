from gevent import monkey
monkey.patch_all()

import requests
import time
import schedule
import threading

from lxml import etree
from gevent.pool import Pool
from queue import Queue

from football.db.mongo_pool import MongoDB
from football.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from football.settings import HEADERS, TEST_INDEX_DATA


"""
    三合一数据
"""
class IndexSpider(object):
    def __init__(self):
        self.redis = Redis_Pool()
        self.mongo_index = MongoDB('football_index')
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        '''异步回调函数'''
        if not self.queue.empty():
            self.coroutine_pool.apply_async(self.__get_data, callback=self.__chech_callbake)

    def get_eventID(self, name):
        datas = self.redis.find(name)
        for k, v in datas.items():
            eventID = eval(k)
            self.queue.put(eventID)
        # 异步调用
        for i in range(TEST_INDEX_DATA):
            if not self.queue.empty():
                self.coroutine_pool.apply_async(self.__get_data, callback=self.__chech_callbake)
        # 守护线程
        self.coroutine_pool.join()

    def __get_data(self):
        proxy = get_ip()
        if not self.queue.empty():
            eventID = self.queue.get()
            msg = {'msg': []}
            msg['赛事ID'] = eventID
            if proxy:
                response = requests.get(f'https://live.leisu.com/3in1-{str(eventID)}', proxies={'http': 'https://'+proxy}, headers=HEADERS).text
            else:
                response = requests.get(f'https://live.leisu.com/3in1-{str(eventID)}', headers=HEADERS).text
            html = etree.HTML(response)
            datas = html.xpath('/html/body/div[1]/div[3]//tr')[1:]
            for data in datas:
                name = data.xpath('./td[2]/span[2]/text()')[0].strip()
                if not name:
                    name = 'Bet365'
                    # name = 'https:' + data.xpath('./td[2]/span[2]/img/@src')[0].strip()
                # 欧指
                ouzhi_1 = data.xpath('./td[3]/div[1]/span/text()')  # 主胜
                if not ouzhi_1:
                    ouzhi_1 = ['', '', '']
                ouzhi_2 = data.xpath('./td[3]/div[2]/span/span/span/text()')  # 主胜
                if not ouzhi_2:
                    ouzhi_2 = ['', '', '']
                # 让球
                rangqiu_1 = data.xpath('./td[4]/div[1]/span/text()')
                if not rangqiu_1:
                    rangqiu_1 = ['', '', '']
                rangqiu_2 = data.xpath('./td[4]/div[2]/span/span/span/text()')
                if not rangqiu_2:
                    rangqiu_2 = ['', '']
                rangqiu_3 = data.xpath('./td[4]/div[2]/span/span[2]/text()')
                if not rangqiu_3:
                    rangqiu_3 = ['']
                # 进球数
                jiqiushu_1 = data.xpath('./td[5]/div[1]/span/text()')
                if not jiqiushu_1:
                    jiqiushu_1 = ['', '', '']
                jiqiushu_2 = data.xpath('./td[5]/div[2]/span/span/span/text()')
                if not jiqiushu_2:
                    jiqiushu_2 = ['', '']
                jiqiushu_3 = data.xpath('./td[5]/div[2]/span/span[2]/text()')
                if not jiqiushu_3:
                    jiqiushu_3 = ['']

                dic = {f'{name}': [{'欧指': {'主胜': [ouzhi_1[0].strip(), ouzhi_2[0].strip()], '和局': [ouzhi_1[1].strip(), ouzhi_2[1].strip()], '客胜': [ouzhi_1[2].strip(), ouzhi_2[2].strip()]}, \
                                    '让球': {'主胜': [rangqiu_1[0].strip(), rangqiu_2[0].strip()], '盘口': [rangqiu_1[1].strip(), rangqiu_3[0].strip()], '客胜': [rangqiu_1[2].strip(), rangqiu_2[1].strip()]}, \
                                    '进球数': {'大球': [jiqiushu_1[0].strip(), jiqiushu_2[0].strip()], '和局': [jiqiushu_1[1].strip(), jiqiushu_3[0].strip()], '小球': [jiqiushu_1[2].strip(), jiqiushu_2[1].strip()]}}]}

                msg['msg'].append(dic)

            # 保存数据
            if msg['msg']:
                self.mongo_index.insert_one(msg, '赛事ID')

    def today_index(self):
        threads = []
        threads.append(threading.Thread(target=self.get_eventID, args=('football_live', )))
        threads.append(threading.Thread(target=self.get_eventID, args=('football_notStart', )))
        threads.append(threading.Thread(target=self.get_eventID, args=('football_finished', )))
        threads.append(threading.Thread(target=self.get_eventID, args=('football_other', )))

        # 开启线程
        for thread in threads:
            thread.start()

        # 守护线程
        for thread in threads:
            thread.join()

    def not_today_index(self):
        threads = []
        threads.append(threading.Thread(target=self.get_eventID, args=('football_history_events', )))
        threads.append(threading.Thread(target=self.get_eventID, args=('football_future_events', )))

        # 开启线程
        for thread in threads:
            thread.start()

        # 守护线程
        for thread in threads:
            thread.join()

    def run(self):
        self.today_index()
        if time.strftime('%H', time.localtime(time.time())) == '00':
            self.not_today_index()
        else:
            pass

    @classmethod
    def start(cls):
        st = cls()
        st.run()
        st.not_today_index()
        # 每隔一段时间执行一次run方法
        schedule.every(10).seconds.do(st.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    IndexSpider.start()
    # index.get_eventID()
    # index.run(1)