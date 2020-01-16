import requests
import re
import schedule
import time

from lxml import etree

from basketball.db.redis_pool import Redis_Pool
from basketball.db.mongo_pool import MongoDB
from IP_API.proxy import get_ip
from basketball.settings import HEADERS


class HomeSpider(object):
    def __init__(self):
        self.redis = Redis_Pool()
        self.mongo = MongoDB('home_info')

    def get_home_data(self):
        try:
            proxy = get_ip()
            if proxy:
                response = requests.get('https://live.leisu.com/lanqiu', proxies={'https': 'https://'+proxy, 'http': 'http://'+proxy} , headers=HEADERS, allow_redirects=False, timeout=3).text
            else:
                response = requests.get('https://live.leisu.com/lanqiu', headers=HEADERS, allow_redirects=False, timeout=3).text
            html = etree.HTML(response)
            # 正在比赛的数据
            lives = html.xpath('//div[@id="live"]/ul/li')
            self._model(lives, 'basketball_live')

            # 未开始比赛的数据
            notStart = html.xpath('//div[@id="notStart"]/ul/li')
            self._model(notStart, 'basketball_notStart')

            # 已经完成的比赛数据
            finished = html.xpath('//div[@id="finished"]/ul/li')
            self._model(finished, 'basketball_finished')
        except Exception as e:
            print(e)

    def _model(self, lives, name):
        data = self._get_dispose_datas(lives)
        # 写入之前清理数据
        self.redis.delete(name)
        for dic in data:
            # 写入数据库
            if dic['mgs']:
                self.redis.insert_one(name, dic['赛事ID'], str(dic))
                self.mongo.insert_one(dic, '赛事ID')

    def _get_dispose_datas(self, lives):
        '''正在比赛的信息'''
        for live in lives:
            dic = {'mgs': []}
            events = live.xpath('.//div[@class="thead row"]/div[1]/span[1]/span/text()')
            if events:
                event = events[0]
            else:
                event = ''
            dic['赛事'] = event
            zhuangtai_1 = live.xpath('.//div[@class="thead row"]/div[1]/span[2]/text()')
            if not zhuangtai_1:
                zhuangtai_1 = ''
            else:
                zhuangtai_1 = zhuangtai_1[0]
            zhuangtai_2 = live.xpath('.//div[@class="thead row"]/div[1]/span[3]/text()')
            if not zhuangtai_2:
                zhuangtai_2 = ''
            else:
                zhuangtai_2 = zhuangtai_2[0]
            zhuangtai = zhuangtai_1 + ' ' + zhuangtai_2
            dic['状态'] = zhuangtai
            times = live.xpath('.//span[@class="time"]/text()')
            if times:
                time = times[0]
            else:
                time = ''
            dic['时间'] = time
            try:
                eventID = re.findall('\d+', live.xpath('.//div[@class="d-row"]/div/div[@class="row"]/a/@href')[0])[0]
            except:
                eventID = ''
            dic['赛事ID'] = eventID
            datas = live.xpath('.//div[@class="d-row"]/div[@class="r-left"]/div')
            for data in datas:
                dat = data.xpath('./div[1]/i[@class="ico"]/@style')
                if dat:
                    logo = 'https:' + re.findall('url\((.*?)\?', dat[0])[0]
                else:
                    logo = ''
                home_team = data.xpath('./div[1]/span[1]/span/text()')
                if home_team:
                    team = home_team[0]
                else:
                    team = ''
                home_1234 = data.xpath('./div[2]/div/text()')
                home_shangxia = data.xpath('./div[3]/text()')
                if home_shangxia:
                    shangxia = home_shangxia[0]
                else:
                    shangxia = ''
                home_quanchang = data.xpath('./b/text()')
                if home_quanchang:
                    quanchang = home_quanchang[0]
                else:
                    quanchang = ''
                home_fencha = data.xpath('./div[4]/text()')
                if home_fencha:
                    fencha = home_fencha[0]
                else:
                    fencha = ''
                team_zongfen = data.xpath('./div[5]/text()')
                if team_zongfen:
                    zongfen_ = team_zongfen[0]
                else:
                    zongfen_ = ''
                home_ouzhi = data.xpath('./div[6]/span/span/text()')
                if home_ouzhi:
                    ouzhi = home_ouzhi[0]
                else:
                    ouzhi = ''
                home_rangfen = data.xpath('./div[7]/div[2]/span/span/text()')
                if home_rangfen:
                    rangfen = home_rangfen[0]
                else:
                    rangfen = ''
                home_zongfen = data.xpath('./div[8]/div[2]/span/span/text()')
                if home_zongfen:
                    zongfen = home_zongfen[0]
                else:
                    zongfen = ''
                dic['mgs'].append({'队名': team, 'LOGO': logo, '1234': home_1234, '上下': shangxia, '全场': quanchang, '分差': fencha, '队总分': zongfen_, '欧指':ouzhi, '让分': rangfen, '总分': zongfen})
            yield dic

    @classmethod
    def start(cls):
        run = cls()
        while True:
            try:
                run.get_home_data()
            except requests.exceptions.ProxyError:
                pass
            # time.sleep(1)


if __name__ == '__main__':
    # home = HomeSpider()
    # home.get_home_data()
    HomeSpider.start()