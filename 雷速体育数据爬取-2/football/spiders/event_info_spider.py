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
from football.settings import HEADERS, TEST_HOME_ASYNC_COUNT


"""
    文字直播及球队信息
"""
class HomePage(object):
    def __init__(self):
        # 建立数据库连接
        self.mongo = MongoDB('football_info')
        self.redis = Redis_Pool()
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        '''异步回调函数'''
        if not self.queue.empty():
            self.coroutine_pool.apply_async(self.__dispose_one_data, callback=self.__chech_callbake)

    def get_data(self, name):
        live = self.redis.find(name)
        for k, v in live.items():
            ID = eval(k)
            self.queue.put(ID)

        for i in range(TEST_HOME_ASYNC_COUNT):
            if not self.queue.empty():
                self.coroutine_pool.apply_async(self.__dispose_one_data, callback=self.__chech_callbake)
                # time.sleep(2)
            # 守护线程
        self.coroutine_pool.join()

    def __dispose_one_data(self):
        proxy = get_ip()
        if not self.queue.empty():
            ID = self.queue.get()
            # 用于储存数据的
            # 文字直播及图片内信息
            info = self._text_broadcast(ID)
            # 球队信息
            info['球队信息'] = self._teams_info(ID)
            # 插入赛事ID
            info['赛事ID'] = ID
            self.mongo.insert_one(info, '赛事ID')

    def _text_broadcast(self, ID):
        res = requests.get('https://api.namitiyu.com/v1/football/match/detail?sid={}'.format(ID)).json()
        msg = {}
        if res:
            # 文字解说
            datas = res['event']
            for data in datas:
                data['data'] = data['data'].replace('雷速体育', '我们')
            # 插入文字解说
            msg['文字解说'] = datas

            if res['stats']:
                # 赛场内容
                corner = res['stats'][0]  # 角球
                yellow_card = res['stats'][1]  # 黄牌
                red_card = res['stats'][2]  # 红牌
                dianqiu = res['stats'][3]  # 点球
                shezheng = res['stats'][4]  # 射正
                shemen = res['stats'][5]  # 射门
                for k, v in shezheng.items():
                    shemen[k] += shezheng[k]
                jingong = res['stats'][6]  # 进攻
                weixianjingong = res['stats'][7]  # 危险进攻
                kongqiulv = res['stats'][8]  # 控球率
                msg['赛场内容'] = {'角球': corner, '黄牌': yellow_card, '红牌': red_card, '点球': dianqiu, '射正': shezheng, '射门': shemen, '进攻': jingong, '危险进攻': weixianjingong, '控球率': kongqiulv}
            else:
                msg['赛场内容'] = '暂无信息'
        # 返回数据
        return msg

    def _teams_info(self, ID):
        res = requests.get('https://api.namitiyu.com/v1/football/match/lineup?tid=1&sid={}'.format(ID)).json()
        msg = {'home': {}, 'away': {}}
        # 左队信息
        if res:
            for datas in res['lineup']['home'][1:]:
                for data in datas:
                    if data[2]:
                        data[2] = 'https:////cdn.leisu.com/avatar/' + data[2]
            msg['home']['msg'] = res['lineup']['home']
            # 右队信息
            for datas in res['lineup']['away'][1:]:
                for data in datas:
                    if data[2]:
                        data[2] = 'https:////cdn.leisu.com/avatar/' + data[2]
            msg['away']['msg'] = res['lineup']['away']
        else:
            msg = '暂无信息'
        return msg

    def today_index(self):
        threads = []
        threads.append(threading.Thread(target=self.get_data, args=('football_live',)))
        threads.append(threading.Thread(target=self.get_data, args=('football_notStart',)))
        threads.append(threading.Thread(target=self.get_data, args=('football_finished',)))
        threads.append(threading.Thread(target=self.get_data, args=('football_other',)))

        # 开启线程
        for thread in threads:
            thread.start()

        # 守护线程
        for thread in threads:
            thread.join()

    def not_today_index(self):
        threads = []
        threads.append(threading.Thread(target=self.get_data, args=('football_history_events', )))
        threads.append(threading.Thread(target=self.get_data, args=('football_future_events', )))

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
        st.not_today_index()
        while True:
            st.today_index()


if __name__ == '__main__':
    HomePage.start()
