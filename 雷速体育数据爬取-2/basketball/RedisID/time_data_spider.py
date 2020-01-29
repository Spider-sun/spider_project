import requests
import re
import time
import threading
import schedule

from lxml import etree

from basketball.db.mongo_pool import MongoDB
from basketball.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from football.settings import TEST_INDEX_DATA, HEADERS


"""
    用于获取历史三天赛事和未来五天赛事
"""
class TimeDataSpider(object):
    def __init__(self):
        # 实例化
        self.mongo = MongoDB('home_page')
        self.redis = Redis_Pool()

    def get_data(self, day):
        if day < 0:
            self._history_one_data(day)
        else:
            self._future_one_data(day)

    def _future_one_data(self, day):
        date = time.strftime('%Y%m%d', time.localtime(time.time() + day * 24 * 3600))
        proxy = get_ip()
        if proxy:
            response = requests.get('https://live.leisu.com/lanqiu/saicheng?date={}'.format(date), headers= HEADERS, proxies={'http': 'https://'+proxy}).text
        else:
            response = requests.get('https://live.leisu.com/lanqiu/saicheng?date={}'.format(date), headers= HEADERS).text
        html = etree.HTML(response)
        datas = html.xpath('//ul[@class="layout-grid-list"]/li')
        for data in datas:
            eventID = data.xpath('./@data-id')[0]  # 赛事ID
            time_ = data.xpath('.//span[@class="time"]/text()')  # 时间
            if time_:
                times = date + time_[0]
            else:
                times = ''
            type_ = data.xpath('.//span[@class="no-state"]/span/text()')  # 状态
            if type_:
                types = type_[0]
            else:
                types = ''
            event = data.xpath('.//div[@class="list-right"]/div[1]/div[1]/span/span/text()')[0]  # 赛事
            # 主场信息
            home_team_ = data.xpath('.//div[@class="r-left"]/div[1]/div[1]//span[@class="lang"]/text()')  # 队名
            if home_team_:
                home_team = home_team_[0]
            else:
                home_team = ''
            home_team_logo__ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[1]//i[@class="ico"]/@style')
            if home_team_logo__:
                home_team_logo_ = home_team_logo__[0]
            else:
                home_team_logo_ = ''
            if home_team_logo_:
                home_team_logo = 'https:' + re.findall('url\((.*?)\?', home_team_logo_)[0]  # 队logo
            else:
                home_team_logo = ''
            home_info_1234 = data.xpath('.//div[@class="r-left"]/div[1]/div[2]/div/text()')  # 1234
            home_shangxia_ = data.xpath('.//div[@class="r-left"]/div[1]/div[3]/text()')  # 上下
            if home_shangxia_:
                home_shangxia = home_shangxia_[0]
            else:
                home_shangxia = ''
            home_quanchang_ = data.xpath('.//div[@class="r-left"]/div[1]/b/text()')  # 全场
            if home_quanchang_:
                home_quanchang = home_quanchang_[0]
            else:
                home_quanchang = ''
            home_fencha_ = data.xpath('.//div[@class="r-left"]/div[1]/div[4]/text()')  # 分差
            if home_fencha_:
                home_fencha = home_fencha_[0]
            else:
                home_fencha = ''
            home_zongfen_ = data.xpath('.//div[@class="r-left"]/div[1]/div[5]/text()')  # 总分
            if home_zongfen_:
                home_zongfen = home_zongfen_[0]
            else:
                home_zongfen = ''
            home_ouzhi_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[6]//span[@class="exponent"]/span[@class="text"]/text()')  # 欧指
            if home_ouzhi_:
                home_ouzhi = home_ouzhi_[0]
            else:
                home_ouzhi = ''
            home_rangfen1_ = data.xpath('.//div[@class="r-left"]/div[1]/div[7]/div[1]/text()')  # 让分
            if home_rangfen1_:
                home_rangfen1 = home_rangfen1_[0]
            else:
                home_rangfen1 = ''
            home_rangfen2_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[7]//span[@class="exponent"]/span/text()')  # 让分
            if home_rangfen2_:
                home_rangfen2 = home_rangfen2_[0]
            else:
                home_rangfen2 = ''
            home_rangfen = home_rangfen1 + ' ' + home_rangfen2  # 让分
            home_hefen1_ = data.xpath('.//div[@class="r-left"]/div[1]/div[8]/div[1]/text()')  # 总分
            if home_hefen1_:
                home_hefen1 = home_hefen1_[0]
            else:
                home_hefen1 = ''
            home_hefen2_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[8]//span[@class="exponent"]/span/text()')  # 总分
            if home_hefen2_:
                home_hefen2 = home_hefen2_[0]
            else:
                home_hefen2 = ''
            home_hefen = home_hefen1 + ' ' + home_hefen2
            # 客场信息
            away_team_ = data.xpath('.//div[@class="r-left"]/div[1]/div[1]//span[@class="lang"]/text()')  # 队名
            if away_team_:
                away_team = away_team_[0]
            else:
                away_team = ''
            away_team_logo__ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[1]//i[@class="ico"]/@style')
            if away_team_logo__:
                away_team_logo_ = away_team_logo__[0]
            else:
                away_team_logo_ = ''
            if away_team_logo_:
                away_team_logo = 'https:' + re.findall('url\((.*?)\?', away_team_logo_)[0]  # 队logo
            else:
                away_team_logo = ''
            away_info_1234 = data.xpath('.//div[@class="r-left"]/div[2]/div[2]/div/text()')  # 1234
            away_shangxia_ = data.xpath('.//div[@class="r-left"]/div[2]/div[3]/text()')  # 上下
            if away_shangxia_:
                away_shangxia = away_shangxia_[0]
            else:
                away_shangxia = ''
            away_quanchang_ = data.xpath('.//div[@class="r-left"]/div[2]/b/text()')  # 全场
            if away_quanchang_:
                away_quanchang = away_quanchang_[0]
            else:
                away_quanchang = ''
            away_fencha_ = data.xpath('.//div[@class="r-left"]/div[2]/div[4]/text()')  # 分差
            if away_fencha_:
                away_fencha = away_fencha_[0]
            else:
                away_fencha = ''
            away_zongfen_ = data.xpath('.//div[@class="r-left"]/div[2]/div[5]/text()')  # 总分
            if away_zongfen_:
                away_zongfen = away_zongfen_[0]
            else:
                away_zongfen = ''
            away_ouzhi_ = data.xpath(
                './/div[@class="r-left"]/div[2]/div[6]//span[@class="exponent"]/span[@class="text"]/text()')  # 欧指
            if away_ouzhi_:
                away_ouzhi = away_ouzhi_[0]
            else:
                away_ouzhi = ''
            away_rangfen1_ = data.xpath('.//div[@class="r-left"]/div[2]/div[7]/div[1]/text()')  # 让分
            if away_rangfen1_:
                away_rangfen1 = away_rangfen1_[0]
            else:
                away_rangfen1 = ''
            away_rangfen2_ = data.xpath(
                './/div[@class="r-left"]/div[2]/div[7]//span[@class="exponent"]/span/text()')  # 让分
            if away_rangfen2_:
                away_rangfen2 = away_rangfen2_[0]
            else:
                away_rangfen2 = ''
            away_rangfen = away_rangfen1 + ' ' + away_rangfen2
            away_hefen1_ = data.xpath('.//div[@class="r-left"]/div[2]/div[8]/div[1]/text()')  # 总分
            if away_hefen1_:
                away_hefen1 = away_hefen1_[0]
            else:
                away_hefen1 = ''
            away_hefen2_ = data.xpath('.//div[@class="r-left"]/div[2]/div[8]//span[@class="exponent"]/span/text()')
            if away_hefen2_:
                away_hefen2 = away_hefen2_[0]
            else:
                away_hefen2 = ''
            away_hefen = away_hefen1 + ' ' + away_hefen2
            dic = {'赛事ID': eventID, '赛事': event, '时间': times, '状态': types,
                   '主队': {'队名': home_team, '队logo': home_team_logo, '1234': home_info_1234, '上下': home_shangxia,
                          '全场': home_quanchang, '分差': home_fencha, '总分': home_zongfen, '欧指': home_ouzhi,
                          '让分': home_rangfen, '合分': home_hefen},
                   '客队': {'队名': away_team, '队logo': away_team_logo, '1234': away_info_1234, '上下': away_shangxia,
                          '全场': away_quanchang, '分差': away_fencha, '总分': away_zongfen, '欧指': away_ouzhi,
                          '让分': away_rangfen, '合分': away_hefen}}
            # 保存数据库
            # if dic['赛事'] != 0:
            self.mongo.insert_one(dic, '赛事ID')
            self.redis.insert_one('basketball_history_events', eventID, eventID)

    def _history_one_data(self, day):
        date = time.strftime('%Y%m%d', time.localtime(time.time() + day * 24 * 3600))
        proxy = get_ip()
        if proxy:
            response = requests.get('https://live.leisu.com/lanqiu/wanchang?date={}'.format(date), headers= HEADERS, proxies={'http': 'https://'+proxy}).text
        else:
            response = requests.get('https://live.leisu.com/lanqiu/wanchang?date={}'.format(date), headers= HEADERS).text
        html = etree.HTML(response)
        datas = html.xpath('//ul[@class="layout-grid-list"]/li')
        for data in datas:
            eventID = data.xpath('./@data-id')[0]  # 赛事ID
            time_ = data.xpath('.//span[@class="time"]/text()')  # 时间
            if time_:
                times = date + time_[0]
            else:
                times = ''
            type_ = data.xpath('.//span[@class="no-state"]/span/text()')  # 状态
            if type_:
                types = type_[0]
            else:
                types = ''
            event_ = data.xpath('.//div[@class="list-right"]/div[1]/div[1]/span/span/text()')  # 赛事
            if event_:
                event = event_[0]
            else:
                event = 0000
            # 主场信息
            home_team_ = data.xpath('.//div[@class="r-left"]/div[1]/div[1]//span[@class="lang"]/text()')  # 队名
            if home_team_:
                home_team = home_team_[0]
            else:
                home_team = ''
            home_team_logo__ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[1]//i[@class="ico"]/@style')
            if home_team_logo__:
                home_team_logo_ = home_team_logo__[0]
            else:
                home_team_logo_ = ''
            if home_team_logo_:
                home_team_logo = 'https:' + re.findall('url\((.*?)\?', home_team_logo_)[0]  # 队logo
            else:
                home_team_logo = ''
            home_info_1234 = data.xpath('.//div[@class="r-left"]/div[1]/div[2]/div/text()')  # 1234
            home_shangxia_ = data.xpath('.//div[@class="r-left"]/div[1]/div[3]/text()')  # 上下
            if home_shangxia_:
                home_shangxia = home_shangxia_[0]
            else:
                home_shangxia = ''
            home_quanchang_ = data.xpath('.//div[@class="r-left"]/div[1]/b/text()')  # 全场
            if home_quanchang_:
                home_quanchang = home_quanchang_[0]
            else:
                home_quanchang = ''
            home_fencha_ = data.xpath('.//div[@class="r-left"]/div[1]/div[4]/text()')  # 分差
            if home_fencha_:
                home_fencha = home_fencha_[0]
            else:
                home_fencha = ''
            home_zongfen_ = data.xpath('.//div[@class="r-left"]/div[1]/div[5]/text()')  # 总分
            if home_zongfen_:
                home_zongfen = home_zongfen_[0]
            else:
                home_zongfen = ''
            home_ouzhi_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[6]//span[@class="exponent"]/span[@class="text"]/text()')  # 欧指
            if home_ouzhi_:
                home_ouzhi = home_ouzhi_[0]
            else:
                home_ouzhi = ''
            home_rangfen1_ = data.xpath('.//div[@class="r-left"]/div[1]/div[7]/div[1]/text()')  # 让分
            if home_rangfen1_:
                home_rangfen1 = home_rangfen1_[0]
            else:
                home_rangfen1 = ''
            home_rangfen2_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[7]//span[@class="exponent"]/span/text()')  # 让分
            if home_rangfen2_:
                home_rangfen2 = home_rangfen2_[0]
            else:
                home_rangfen2 = ''
            home_rangfen = home_rangfen1 + ' ' + home_rangfen2  # 让分
            home_hefen1_ = data.xpath('.//div[@class="r-left"]/div[1]/div[8]/div[1]/text()')  # 总分
            if home_hefen1_:
                home_hefen1 = home_hefen1_[0]
            else:
                home_hefen1 = ''
            home_hefen2_ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[8]//span[@class="exponent"]/span/text()')  # 总分
            if home_hefen2_:
                home_hefen2 = home_hefen2_[0]
            else:
                home_hefen2 = ''
            home_hefen = home_hefen1 + ' ' + home_hefen2
            # 客场信息
            away_team_ = data.xpath('.//div[@class="r-left"]/div[1]/div[1]//span[@class="lang"]/text()')  # 队名
            if away_team_:
                away_team = away_team_[0]
            else:
                away_team = ''
            away_team_logo__ = data.xpath(
                './/div[@class="r-left"]/div[1]/div[1]//i[@class="ico"]/@style')
            if away_team_logo__:
                away_team_logo_ = away_team_logo__[0]
            else:
                away_team_logo_ = ''
            if away_team_logo_:
                away_team_logo = 'https:' + re.findall('url\((.*?)\?', away_team_logo_)[0]  # 队logo
            else:
                away_team_logo = ''
            away_info_1234 = data.xpath('.//div[@class="r-left"]/div[2]/div[2]/div/text()')  # 1234
            away_shangxia_ = data.xpath('.//div[@class="r-left"]/div[2]/div[3]/text()')  # 上下
            if away_shangxia_:
                away_shangxia = away_shangxia_[0]
            else:
                away_shangxia = ''
            away_quanchang_ = data.xpath('.//div[@class="r-left"]/div[2]/b/text()')  # 全场
            if away_quanchang_:
                away_quanchang = away_quanchang_[0]
            else:
                away_quanchang = ''
            away_fencha_ = data.xpath('.//div[@class="r-left"]/div[2]/div[4]/text()')  # 分差
            if away_fencha_:
                away_fencha = away_fencha_[0]
            else:
                away_fencha = ''
            away_zongfen_ = data.xpath('.//div[@class="r-left"]/div[2]/div[5]/text()')  # 总分
            if away_zongfen_:
                away_zongfen = away_zongfen_[0]
            else:
                away_zongfen = ''
            away_ouzhi_ = data.xpath(
                './/div[@class="r-left"]/div[2]/div[6]//span[@class="exponent"]/span[@class="text"]/text()')  # 欧指
            if away_ouzhi_:
                away_ouzhi = away_ouzhi_[0]
            else:
                away_ouzhi = ''
            away_rangfen1_ = data.xpath('.//div[@class="r-left"]/div[2]/div[7]/div[1]/text()')  # 让分
            if away_rangfen1_:
                away_rangfen1 = away_rangfen1_[0]
            else:
                away_rangfen1 = ''
            away_rangfen2_ = data.xpath(
                './/div[@class="r-left"]/div[2]/div[7]//span[@class="exponent"]/span/text()')  # 让分
            if away_rangfen2_:
                away_rangfen2 = away_rangfen2_[0]
            else:
                away_rangfen2 = ''
            away_rangfen = away_rangfen1 + ' ' + away_rangfen2
            away_hefen1_ = data.xpath('.//div[@class="r-left"]/div[2]/div[8]/div[1]/text()')  # 总分
            if away_hefen1_:
                away_hefen1 = away_hefen1_[0]
            else:
                away_hefen1 = ''
            away_hefen2_ = data.xpath('.//div[@class="r-left"]/div[2]/div[8]//span[@class="exponent"]/span/text()')
            if away_hefen2_:
                away_hefen2 = away_hefen2_[0]
            else:
                away_hefen2 = ''
            away_hefen = away_hefen1 + ' ' + away_hefen2
            dic = {'赛事ID': eventID, '赛事': event, '时间': times, '状态': types,
                   '主队': {'队名': home_team, '队logo': home_team_logo, '1234': home_info_1234, '上下': home_shangxia,
                          '全场': home_quanchang, '分差': home_fencha, '总分': home_zongfen, '欧指': home_ouzhi,
                          '让分': home_rangfen, '合分': home_hefen},
                   '客队': {'队名': away_team, '队logo': away_team_logo, '1234': away_info_1234, '上下': away_shangxia,
                          '全场': away_quanchang, '分差': away_fencha, '总分': away_zongfen, '欧指': away_ouzhi,
                          '让分': away_rangfen, '合分': away_hefen}}
            # 保存数据库
            # if dic['赛事'] != 0:
            self.mongo.insert_one(dic, '赛事ID')
            self.redis.insert_one('basketball_future_events', eventID, eventID)

    def run(self):
        threads = []
        for i in range(-3, 6):
            if i != 0:
                thread = threading.Thread(target=self.get_data, args=(i,))
                threads.append(thread)
                # 启动线程
                thread.start()
            else:
                continue
            # 守护线程
        for thread in threads:
            thread.join()
        # self.get_data(-2)

    @classmethod
    def start(cls):
        st = cls()

        def ss():
            if time.strftime('%H', time.localtime(time.time())) == '00':
                st.run()

        st.run()
        # 每隔一段时间执行一次run方法
        schedule.every(600).seconds.do(ss)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    timedata = TimeDataSpider()
    timedata.run()