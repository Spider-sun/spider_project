from gevent import monkey
monkey.patch_all()

import requests
import threading
import time

from queue import Queue
from gevent.pool import Pool

from basketball.db.mongo_pool import MongoDB
from basketball.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from basketball.settings import HEADERS, NEW_THREADING


"""
    文字直播及球员信息
"""
class NewSpider(object):
    def __init__(self):
        self.redis = Redis_Pool()
        self.mongo = MongoDB('detail')
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        '''异步回调函数'''
        if not self.queue.empty():
            self.coroutine_pool.apply_async(self.get_response, callback=self.__chech_callbake)

    def get_ID(self, name):
        datas = self.redis.find(name)
        for k, v in datas.items():
            try:
                ID = eval(k)
                self.queue.put(ID)
            except:
                pass

        for i in range(NEW_THREADING):
            if not self.queue.empty():
                self.coroutine_pool.apply_async(self.get_response, callback=self.__chech_callbake)
                # time.sleep(2)
            # 守护线程
        self.coroutine_pool.join()

    def get_response(self):
        if not self.queue.empty():
            ID = self.queue.get()
            proxy = get_ip()
            if proxy:
                response = requests.get('https://api.namitiyu.com/v1/basketball/match/detail?sid={}&lang=zh'.format(ID), proxies={'https': 'https://'+proxy, 'http': 'http://'+proxy} , headers=HEADERS).json()
            else:
                response = requests.get('https://api.namitiyu.com/v1/basketball/match/detail?sid={}&lang=zh'.format(ID), headers=HEADERS).json()
            msg = {}
            msg['赛事ID'] = ID
            # 文字直播
            dic_text = self.get_text_broadcas(response)
            msg['文字直播'] = dic_text
            # 球员信息
            dic_players = self.get_player(response)
            msg['球员信息'] = dic_players
            # 插入数据库
            self.mongo.insert_one(msg, '赛事ID')
            # 调度队列的tesk_done方法
            self.queue.task_done()

    def get_text_broadcas(self, response):
        '''文字直播'''
        msg = {'msg': {}}
        text_ls_data = response['data']['tlive']
        if not text_ls_data:
            msg['msg'] = '暂无信息'
        else:
            for i in range(len(text_ls_data)):
                msg['msg']['第{}节'.format(i + 1)] = text_ls_data[i]
        return msg

    def get_player(self, response):
        '''获取球员信息'''
        msg = {'msg': {}}
        text_ls_data = response['data']['players']
        if not text_ls_data:
            msg['msg'] = '暂无信息'
        else:
            for text_ls in text_ls_data[0:2]:
                for text in text_ls:
                    text[4] = 'https://cdn.leisu.com/basketball/player/' + text[4]
                    data = text[6].split('^')
                    if data[-1] == 0:
                        text[6] = '是^' + text[6][0:-4]
            msg['msg'] = text_ls_data
        return msg

    def run_today(self):
        threads = []
        threads.append(threading.Thread(target=self.get_ID, args=('basketball_live',)))
        threads.append(threading.Thread(target=self.get_ID, args=('basketball_notStart',)))
        threads.append(threading.Thread(target=self.get_ID, args=('basketball_finished',)))
        # 开启线程
        for thread in threads:
            thread.start()
        # 守护线程
        for thread in threads:
            thread.join()

    @classmethod
    def start(cls):
        st = cls()
        while True:
            st.run_today()


if __name__ == '__main__':
    # new = NewSpider()
    # new.get_ID()
    # new.get_response()
    NewSpider.start()