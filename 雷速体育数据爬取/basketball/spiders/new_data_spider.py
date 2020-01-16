from gevent import monkey
monkey.patch_all()

import requests
import time

from lxml import etree
from queue import Queue
from gevent.pool import Pool

from basketball.db.mongo_pool import MongoDB
from basketball.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from basketball.settings import HEADERS, NEW_THREADING


class NewSpider(object):
    def __init__(self):
        self.redis = Redis_Pool()
        self.mongo = {
            'home_infos' :MongoDB('home_infos'),
            'news_text_broadcas' :MongoDB('news_text_broadcas'),
            'new_players_info' :MongoDB('new_players_info')
        }
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        '''异步回调函数'''
        if not self.queue.empty():
            self.coroutine_pool.apply_async(self.get_response, callback=self.__chech_callbake)

    def get_ID(self):
        datas = self.redis.find('basketball_live')
        print(datas)
        for k, v in datas.items():
            ID = eval(k)
            self.queue.put(ID)

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
                response = requests.get('https://live.leisu.com/lanqiu/detail-{}'.format(ID), proxies={'https': 'https://'+proxy, 'http': 'http://'+proxy} , headers=HEADERS, allow_redirects=False).text
            else:
                response = requests.get('https://live.leisu.com/lanqiu/detail-{}'.format(ID), headers=HEADERS, allow_redirects=False).text
            html = etree.HTML(response)
            # 文字直播
            self.get_text_broadcas(html, ID)
            # 球员信息
            self.get_player(html, ID)
            # 调度队列的tesk_done方法
            self.queue.task_done()

    def get_text_broadcas(self, html, ID):
        '''文字直播'''
        msg = {'文字直播': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@class="nano-content"]/ul[@class="list-content"]/li')
        if not datas:
            msg['文字直播'] = '暂无信息'
        else:
            for data in datas:
                time = data.xpath('./div[@class="code"]/text()')[0]
                score = str(data.xpath('./div[@class="score"]/span/text()')).replace(',', '-')[1:-1]
                tip = data.xpath('./div[@class="tip"]/text()')[0]
                msg['文字直播'].append({'时间': time, '比分': score, '文字描述': tip})
        # 保存
        self.mongo['news_text_broadcas'].insert_one(msg, '赛事ID')

    def get_player(self, html, ID):
        '''获取球员信息'''
        msg = {'人员信息': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@class="content clearfix"]/div')
        for data in datas[2:]:
            ms = {}
            team = data.xpath('./div[@class="logo-name"]/div[@class="name"]/text()')
            if team:
                ms['队名'] = team[0]
            else:
                ms['队名'] = ''
            # 获取球队得失信息
            team_infos = self._get_info(data)
            ms['球队总体信息'] = team_infos
            # 获取球员信息
            players_infos = [player for player in self._get_player_info(data)]
            ms['球员信息'] = players_infos
            # 添加列表
            msg['人员信息'].append(ms)
        print(msg)
        # 保存
        self.mongo['new_players_info'].insert_one(msg, '赛事ID')

    def _get_player_info(self, data):
        players = []
        infos = data.xpath('./div[@class="sp-tb"]/div[@class="list"]/div')
        for info in infos[1:]:
            dic = {}
            beihao = info.xpath('./div[1]/span/text()')
            if beihao:
                dic['背号'] = beihao[0]
            else:
                dic['背号'] = ''
            name = info.xpath('./div[2]//span[@class="o-hidden name"]/text()')
            if name:
                dic['姓名'] = name[0]
            else:
                dic['姓名'] = ''
            shoufa = info.xpath('./div[3]/span/text()')
            if shoufa:
                dic['首发'] = shoufa[0]
            else:
                dic['首发'] = ''
            chuchangshijian = info.xpath('./div[4]/span/text()')
            if chuchangshijian:
                dic['出场时间'] = chuchangshijian[0]
            else:
                dic['出场时间'] = ''
            toulan = info.xpath('./div[5]/span/text()')
            if toulan:
                dic['投篮'] = toulan[0]
            else:
                dic['投篮'] = ''
            sanfen = info.xpath('./div[6]/span/text()')
            if sanfen:
                dic['三分'] = sanfen[0]
            else:
                dic['三分'] = ''
            faqiu = info.xpath('./div[7]/span/text()')
            if faqiu:
                dic['罚球'] = faqiu[0]
            else:
                dic['罚球'] = ''
            qianlanban = info.xpath('./div[8]/span/text()')
            if qianlanban:
                dic['前篮板'] = qianlanban[0]
            else:
                dic['前篮板'] = ''
            houlanban = info.xpath('./div[9]/span/text()')
            if houlanban:
                dic['后篮板'] = houlanban[0]
            else:
                dic['后篮板'] = ''
            zonglanban = info.xpath('./div[10]/span/text()')
            if zonglanban:
                dic['总篮板'] = zonglanban[0]
            else:
                dic['总篮板'] = ''
            zhugong = info.xpath('./div[11]/span/text()')
            if zhugong:
                dic['助攻'] = zhugong[0]
            else:
                dic['助攻'] = ''
            qiangduan = info.xpath('./div[12]/span/text()')
            if qiangduan:
                dic['抢断'] = qiangduan[0]
            else:
                dic['抢断'] = ''
            gaimao = info.xpath('./div[13]/span/text()')
            if gaimao:
                dic['盖帽'] = gaimao[0]
            else:
                dic['盖帽'] = ''
            shiwu = info.xpath('./div[14]/span/text()')
            if shiwu:
                dic['失误'] = shiwu[0]
            else:
                dic['失误'] = ''
            fangui = info.xpath('./div[15]/span/text()')
            if fangui:
                dic['犯规'] = fangui[0]
            else:
                dic['犯规'] = ''
            defen = info.xpath('./div[16]/span/text()')
            if defen:
                dic['得分'] = defen[0]
            else:
                dic['得分'] = ''
            yield dic

            players.append(dic)
        return players

    def _get_info(self, data):
        # 获取总体情况
        dic = {}
        messages = data.xpath('./div[@class="sp-tb"]/div[@class="summary"]/div[@class="row totals "]')
        if not messages:
            pass
        else:
            defen = messages[0].xpath('./div[1]/span/text()')
            if defen:
                dic['得分'] = defen[0]
            else:
                dic['得分'] = ''
            zhugong = messages[0].xpath('./div[2]/span/text()')
            if zhugong:
                dic['助攻'] = zhugong[0]
            else:
                dic['助攻'] = ''
            lanban = messages[0].xpath('./div[3]/span/text()')
            if lanban:
                dic['篮板'] = lanban[0]
            else:
                dic['篮板'] = ''
            qianhoulanban = messages[0].xpath('./div[4]/span/text()')
            if qianhoulanban:
                dic['前-后篮板'] = qianhoulanban[0]
            else:
                dic['前-后篮板'] = ''
            duanqiang = messages[0].xpath('./div[5]/span/text()')
            if duanqiang:
                dic['抢断'] = duanqiang[0]
            else:
                dic['抢断'] = ''
            gaimao = messages[0].xpath('./div[6]/span/text()')
            if gaimao:
                dic['盖帽'] = gaimao[0]
            else:
                dic['盖帽'] = ''
            toulan = messages[0].xpath('./div[7]/span/text()')
            if toulan:
                dic['投篮( 中 - 投 )'] = toulan[0]
            else:
                dic['投篮( 中 - 投 )'] = ''
            sanfen = messages[0].xpath('./div[8]/span/text()')
            if sanfen:
                dic['三分'] = sanfen[0]
            else:
                dic['三分'] = ''
            faqiu = messages[0].xpath('./div[9]/span/text()')
            if faqiu:
                dic['罚球( 中 - 投 )'] = faqiu[0]
            else:
                dic['罚球( 中 - 投 )'] = ''
            shiwu = messages[0].xpath('./div[10]/span/text()')
            if shiwu:
                dic['失误'] = shiwu[0]
            else:
                dic['失误'] = ''
            fangui = messages[0].xpath('./div[11]/span/text()')
            if fangui:
                dic['犯规'] = fangui[0]
            else:
                dic['犯规'] = ''
        return dic

    @classmethod
    def start(cls):
        run = cls()
        while True:
            # try:
                run.get_ID()
            # except requests.exceptions.ProxyError:
            #     pass
            # time.sleep(1)


if __name__ == '__main__':
    # new = NewSpider()
    # new.get_ID()
    # new.get_response()
    NewSpider.start()