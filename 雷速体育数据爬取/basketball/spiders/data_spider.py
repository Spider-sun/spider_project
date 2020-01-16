from gevent import monkey
monkey.patch_all()

import requests
import schedule
import time

from lxml import etree
from queue import Queue
from gevent.pool import Pool

from basketball.db.mongo_pool import MongoDB
from basketball.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from basketball.settings import HEADERS, DATA_THREADING, DATA_LIVE_TIME


class DataSpider(object):
    def __init__(self):
        # 联赛积分
        self.mongo = {
            'league-points': MongoDB('league-points'),
            'technical-statistics': MongoDB('technical-statistics'),
            'historical': MongoDB('historical'),
            'recent-record': MongoDB('recent-record'),
            'fixture': MongoDB('fixture')
            }
        self.redis = Redis_Pool()
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
            ID = eval(k)
            self.queue.put(ID)

        for i in range(DATA_THREADING):
            if not self.queue.empty():
                self.coroutine_pool.apply_async(self.get_response, callback=self.__chech_callbake)
                # time.sleep(2)
            # 守护线程
        self.coroutine_pool.join()

    def get_response(self):
        if not self.queue.empty():
            ID = self.queue.get()
            proxy = get_ip()
            try:
                if proxy:
                    try:
                        response = requests.get('https://live.leisu.com/lanqiu/shujufenxi-{}'.format(ID), proxies={'https': 'https://'+proxy, 'http': 'http://'+proxy} , headers=HEADERS, allow_redirects=False)
                    except:
                        response = requests.get('https://live.leisu.com/lanqiu/shujufenxi-{}'.format(ID), proxies={'https': 'https://'+proxy, 'http': 'http://'+proxy} , headers=HEADERS, allow_redirects=False, verify=False)
                else:
                    try:
                        response = requests.get('https://live.leisu.com/lanqiu/shujufenxi-{}'.format(ID), headers=HEADERS, allow_redirects=False)
                    except:
                        response = requests.get('https://live.leisu.com/lanqiu/shujufenxi-{}'.format(ID), headers=HEADERS, allow_redirects=False, verify=False)
                html = etree.HTML(response.text)
                # 联赛积分
                self._league_points(html, ID)
                # 技术统计
                self._technical_statistics(html, ID)
                # 近期战绩
                self._historical(html, ID)
                # 近期战绩
                self._recent_record(html, ID)
                # 未来赛程
                self._fixture(html, ID)
                # 调度队列的tesk_done方法
                self.queue.task_done()
            except requests.exceptions.ProxyError:
                pass

    def _league_points(self, html, ID):
        '''联赛积分'''
        msg = {'联赛积分': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@id="league-points"]/div[2]/div')
        if len(datas) < 2:
            msg['联赛积分'] = '暂无数据'
        else:
            for data in datas:
                dic = {'msg': []}
                team = data.xpath('.//span[@class="name"]/text()')[0]
                dic['队名'] = team
                rank = data.xpath('.//div[@class="float-left f-s-12 color-999 line-h-25"]/text()')[0]
                dic['排名'] = rank
                das = data.xpath('.//tr')[1:]
                for da in das:
                    type_ls = da.xpath('./td[1]/text()')  # 类型
                    if type_ls:
                        type = type_ls[0].strip()
                    else:
                        type = ''
                    sai_ls = da.xpath('./td[2]/text()')  # 赛
                    if sai_ls:
                        sai = sai_ls[0].strip()
                    else:
                        sai = ''
                    sheng_ls = da.xpath('./td[3]/text()')  # 胜
                    if sheng_ls:
                        sheng = sheng_ls[0].strip()
                    else:
                        sheng = ''
                    fu_ls = da.xpath('./td[4]/text()')  # 负
                    if fu_ls:
                        fu = fu_ls[0].strip()
                    else:
                        fu = ''
                    defen_ls = da.xpath('./td[5]/text()')  # 得分
                    if defen_ls:
                        defen = defen_ls[0].strip()
                    else:
                        defen = ''
                    shifen_ls = da.xpath('./td[6]/text()')  # 失分
                    if shifen_ls:
                        shifen = shifen_ls[0].strip()
                    else:
                        shifen = ''
                    jingshengfen_ls = da.xpath('./td[7]/text()')  # 净胜分
                    if jingshengfen_ls:
                        jingshengfen = jingshengfen_ls[0].strip()
                    else:
                        jingshengfen = ''
                    paiming_ls = da.xpath('./td[8]/text()')  # 排名
                    if paiming_ls:
                        paiming = paiming_ls[0].strip()
                    else:
                        paiming = ''
                    shenglv_ls = da.xpath('./td[9]/text()')  # 胜率
                    if shenglv_ls:
                        shenglv = shenglv_ls[0].strip()
                    else:
                        shenglv = ''
                    dic['msg'].append({'类型': type, '赛': sai, '胜': sheng, '负': fu, '得分': defen, '失分': shifen, '净胜分': jingshengfen, '排名': paiming, '胜率': shenglv})
                msg['联赛积分'].append(dic)

        self.mongo["league-points"].insert_one(msg, '赛事ID')

    def _technical_statistics(self, html, ID):
        '''技术统计'''
        msg = {'技术统计': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@id="technical-statistics"]/div[2]/div')
        if not datas:
            msg['技术统计'] = '暂无数据'
        else:
            for data in datas[1:]:
                dic = {'msg': []}
                team = data.xpath('.//span[@class="name"]/text()')[0]
                dic['队名'] = team
                das = data.xpath('.//tr')[1:]
                for da in das:
                    type_ls = da.xpath('./td[1]/text()')  # 类型
                    if type_ls:
                        type = type_ls[0].strip()
                    else:
                        type = ''
                    sai_ls = da.xpath('./td[2]/text()')  # 投篮命中率
                    if sai_ls:
                        sai = sai_ls[0].strip()
                    else:
                        sai = ''
                    sheng_ls = da.xpath('./td[3]/text()')  # 三分命中率
                    if sheng_ls:
                        sheng = sheng_ls[0].strip()
                    else:
                        sheng = ''
                    fu_ls = da.xpath('./td[4]/text()')  # 平均篮板
                    if fu_ls:
                        fu = fu_ls[0].strip()
                    else:
                        fu = ''
                    defen_ls = da.xpath('./td[5]/text()')  # 平均助攻
                    if defen_ls:
                        defen = defen_ls[0].strip()
                    else:
                        defen = ''
                    shifen_ls = da.xpath('./td[6]/text()')  # 平均抢断
                    if shifen_ls:
                        shifen = shifen_ls[0].strip()
                    else:
                        shifen = ''
                    jingshengfen_ls = da.xpath('./td[7]/text()')  # 平均失误
                    if jingshengfen_ls:
                        jingshengfen = jingshengfen_ls[0].strip()
                    else:
                        jingshengfen = ''

                    dic['msg'].append(
                        {'类型': type, '投篮命中率': sai, '三分命中率': sheng, '平均篮板': fu, '平均助攻': defen, '平均抢断': shifen, '平均失误': jingshengfen})
                msg['技术统计'].append(dic)

        self.mongo["technical-statistics"].insert_one(msg, '赛事ID')

    def _historical(self, html, ID):
        '''历史交锋'''
        msg = {'历史交锋': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@id="historical"]/div[2]//tr')
        if not datas:
            msg['历史交锋'] = '暂无数据'
        else:
            for data in datas[1:]:
                event = data.xpath('./td[1]/a/text()')[0]  # 赛事
                time = data.xpath('./td[2]/text()')[0].strip()  # 比赛时间
                away_team = data.xpath('./td[3]/a/span/text()')[0]  # 客队
                score = str(data.xpath('./td[4]/a/span/text()')).replace(',', ':')[1:-1]  # 比分
                home_team = data.xpath('./td[5]/a/span/text()')[0]  # 主队
                shengfu = data.xpath('./td[6]/span/text()')[0].strip()  # 胜负
                fencha = data.xpath('./td[7]/text()')[0].strip()  # 分差
                rangfen = data.xpath('./td[8]/text()')[0].strip()  # 让分
                panlu_ls = data.xpath('./td[9]/span/text()')  # 盘路
                if panlu_ls:
                    panlu = panlu_ls[0].strip()
                else:
                    panlu = ''
                zongfen = data.xpath('./td[10]/text()')[0].strip()  # 总分
                zongfenpan = data.xpath('./td[11]/text()')[0].strip()  # 总分盘
                jinqiushu_ls = data.xpath('./td[12]/span/text()')  # 进球数
                if jinqiushu_ls:
                    jinqiushu = jinqiushu_ls[0].strip()
                else:
                    jinqiushu = ''

                msg['历史交锋'].append({'赛事': event, '比赛时间': time, '客队': away_team, '比分': score, '主队': home_team, '胜负': shengfu, '分差': fencha, '让分': rangfen, '盘路': panlu, '总分': zongfen, '总分盘': zongfenpan, '进球数': jinqiushu})

        self.mongo["historical"].insert_one(msg, '赛事ID')

    def _recent_record(self, html, ID):
        '''近期战绩'''
        msg = {'近期战绩': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@id="recent-record"]/div[2]/div')
        # if not datas:
        #     msg['近期战绩'] = '暂无数据'
        # else:
        for data in datas:
            team_ls = data.xpath('.//span[@class="name"]/text()')
            if team_ls:
                team = team_ls[0]
            else:
                team = ''
            dic = {'战队': team, 'msg': []}
            dats = data.xpath('.//tr')[1:]
            for dat in dats:
                event = dat.xpath('./td[1]/a/text()')[0]  # 赛事
                time = dat.xpath('./td[2]/text()')[0].strip()  # 比赛时间
                away_team = dat.xpath('./td[3]/a/span/text()')[0]  # 客队
                score = str(dat.xpath('./td[4]/a/span/text()')).replace(',', ':')[1:-1]  # 比分
                home_team = dat.xpath('./td[5]/a/span/text()')[0]  # 主队
                shengfu = dat.xpath('./td[6]/span/text()')[0].strip()  # 胜负
                fencha = dat.xpath('./td[7]/text()')[0].strip()  # 分差
                rangfen = dat.xpath('./td[8]/text()')[0].strip()  # 让分
                panlu_ls = dat.xpath('./td[9]/span/text()')  # 盘路
                if panlu_ls:
                    panlu = panlu_ls[0].strip()
                else:
                    panlu = ''
                zongfen = dat.xpath('./td[10]/text()')[0].strip()  # 总分
                zongfenpan = dat.xpath('./td[11]/text()')[0].strip()  # 总分盘
                jinqiushu_ls = dat.xpath('./td[12]/span/text()')  # 进球数
                if jinqiushu_ls:
                    jinqiushu = jinqiushu_ls[0].strip()
                else:
                    jinqiushu = ''

                dic['msg'].append(
                    {'赛事': event, '比赛时间': time, '客队': away_team, '比分': score, '主队': home_team, '胜负': shengfu, '分差': fencha,
                     '让分': rangfen, '盘路': panlu, '总分': zongfen, '总分盘': zongfenpan, '进球数': jinqiushu})
            msg['近期战绩'].append(dic)
        self.mongo["recent-record"].insert_one(msg, '赛事ID')

    def _fixture(self, html, ID):
        '''未来赛程'''
        msg = {'未来赛程': []}
        msg['赛事ID'] = ID
        datas = html.xpath('//div[@id="fixture"]/div[2]/div')
        for data in datas:
            team_ls = data.xpath('.//span[@class="name"]/text()')
            if team_ls:
                team = team_ls[0]
            else:
                team = ''
            dic = {'战队': team, 'msg': []}
            dats = data.xpath('.//table/tr')
            if len(dats) > 1:
                for dat in dats[1:]:
                    event = dat.xpath('./td[1]/span/text()')[0]  # 赛事
                    time = dat.xpath('./td[2]/text()')[0].strip()  # 比赛时间
                    away_team = dat.xpath('./td[3]/text()')[0]  # 客队
                    home_team = dat.xpath('./td[4]/text()')[0]  # 主队
                    time_speed = dat.xpath('./td[5]/text()')[0]  # 与本场相隔

                    dic['msg'].append(
                        {'赛事': event, '比赛时间': time, '客队': away_team, '主队': home_team, '与本场相隔': time_speed})
                msg['未来赛程'].append(dic)
        self.mongo["fixture"].insert_one(msg, '赛事ID')

    @classmethod
    def start(cls):
        '''未开始或已经结束'''
        run = cls()
        def run_notLive():
            run.get_ID('basketball_notStart')
            run.get_ID('basketball_finished')
            run.get_ID('basketball_live')
        run_notLive()
        # 每隔一段时间执行一次run方法
        schedule.every(DATA_LIVE_TIME).seconds.do(run_notLive)
        while True:
            schedule.run_pending()
            time.sleep(1)




if __name__ == '__main__':
    # data = DataSpider()
    # data.get_ID('basketball_live')
    DataSpider.start()
    # data.get_response(3506053)
    # DataSpider.start()