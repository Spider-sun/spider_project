import requests
import time
import re
import threading
import schedule

from lxml import etree

from football.db.redis_pool import Redis_Pool
from football.db.mongo_pool import MongoDB
from IP_API.proxy import get_ip
from football.settings import TEST_INDEX_DATA, HEADERS


"""
    历史及未来赛事
"""
class TimeDataSpider(object):
    def __init__(self):
        self.redis = Redis_Pool()
        self.mongo = MongoDB('home_page')

    def get_response(self, day):
        if day < 0:
            self._history_one_data(day)
        else:
            self._future_one_data(day)

    def _history_one_data(self, day):
        date = time.strftime('%Y%m%d', time.localtime(time.time() + day * 24 * 3600))
        proxy = get_ip()
        if proxy:
            response = requests.get('https://live.leisu.com/wanchang?date={}'.format(date), headers= HEADERS, proxies={'http': 'https://'+proxy}).text
        else:
            response = requests.get('https://live.leisu.com/wanchang?date={}'.format(date), headers= HEADERS).text
        html = etree.HTML(response)
        datas = html.xpath('//*[@id="finished"]/ul/li')
        for data in datas:
            event_ID = data.xpath('./@data-id')[0]  # 赛事ID
            event_LOGO_ = data.xpath('.//span[@class="lab-events"]/span/@style')  # 赛事LOGO
            if event_LOGO_:
                event_LOGO = 'https:' + re.findall('url\((.*?)\?', event_LOGO_[0])[0]
            else:
                event_LOGO = ''
            event_ = data.xpath('.//a[@class="event-name"]/span/text()')  # 赛事
            if event_:
                event = event_[0]
            else:
                event = ''
            count_ = data.xpath('.//span[@class="lab-round"]/text()')  # 轮次
            if count_:
                count = count_[0]
            else:
                count = ''
            event_time_ = data.xpath('.//span[@class="lab-time"]/text()')  # 比赛时间
            if event_time_:
                event_time = date + event_time_[0]
            else:
                event_time = ''
            team_home_ = data.xpath('.//span[@class="lab-team-home"]/span/a/text()')  # 主场球队
            if team_home_:
                team_home = team_home_[0]
            else:
                team_home = ''
            team_home_ID_ = data.xpath('.//span[@class="lab-team-home"]/span/a/@href')  # 主场球队ID
            if team_home_ID_:
                team_home_ID = team_home_ID_[0].split('-')[-1]
            else:
                team_home_ID = ''
            score_ = data.xpath('.//span[@class="score"]/b/text()')  # 比分
            if score_:
                score = score_[0]
            else:
                score = ''
            team_away_ = data.xpath('.//span[@class="lab-team-away"]/span/a/text()')  # 客场球队
            if team_away_:
                team_away = team_away_[0]
            else:
                team_away = ''
            team_away_ID_ = data.xpath('.//span[@class="lab-team-away"]/span/a/@href')  # 客场球队ID
            if team_away_ID_:
                team_away_ID = team_away_ID_[0].split('-')[-1]
            else:
                team_away_ID = ''
            lab_half_ = data.xpath('.//span[@class="lab-half"]/text()')  # 半场
            if lab_half_:
                lab_half = lab_half_[0]
            else:
                lab_half = ''

            lab_corner_ = data.xpath('.//span[@class="lab-corner"]/span/text()')  # 角球
            if lab_corner_:
                lab_corner = lab_corner_[0]
            else:
                lab_corner = ''
            lab_bet_dds_ = data.xpath('.//span[@class="lab-bet-odds"]/span/text()')  # 胜负
            if lab_bet_dds_:
                lab_bet_dds = lab_bet_dds_[0]
            else:
                lab_bet_dds = ''
            lab_ratel_ = data.xpath('.//span[@class="lab-ratel"]/text()')  # 让球
            if lab_ratel_:
                lab_ratel = lab_ratel_[0]
            else:
                lab_ratel = ''
            lab_size_ = data.xpath('.//span[@class="lab-size"]/span/text()')  # 进球数
            if lab_size_:
                lab_size = lab_size_[0]
            else:
                lab_size = ''
            dic = {'赛事ID': event_ID, '赛事LOGO': event_LOGO, '赛事': event, '轮次': count, '比赛时间': event_time, '主场球队': team_home,
                           '主场球队ID': team_home_ID, '比分': score, '客场球队': team_away, '客场球队ID': team_away_ID,
                           '半场': lab_half, '角球': lab_corner, '胜负': lab_bet_dds, '让球': lab_ratel, '进球数': lab_size}
            # 保存数据库
            self.mongo.insert_one(dic, '赛事ID')
            self.redis.insert_one('football_history_events', event_ID, event_ID)

    def _future_one_data(self, day):
        date = time.strftime('%Y%m%d', time.localtime(time.time() + day * 24 * 3600))
        proxy = get_ip()
        if proxy:
            response = requests.get('https://live.leisu.com/saicheng?date={}'.format(date), headers= HEADERS, proxies={'http': 'https://'+proxy}).text
        else:
            response = requests.get('https://live.leisu.com/saicheng?date={}'.format(date), headers= HEADERS).text
        html = etree.HTML(response)
        datas = html.xpath('//*[@id="notStart"]/ul/li')
        for data in datas:
            event_ID = data.xpath('./@data-id')[0]  # 赛事ID
            event_LOGO_ = data.xpath('.//span[@class="lab-events"]/span/@style')  # 赛事LOGO
            if event_LOGO_:
                event_LOGO = 'https:' + re.findall('url\((.*?)\?', event_LOGO_[0])[0]
            else:
                event_LOGO = ''
            event_ = data.xpath('.//a[@class="event-name"]/span/text()')  # 赛事
            if event_:
                event = event_[0]
            else:
                event = ''
            count_ = data.xpath('.//span[@class="lab-round"]/text()')  # 轮次
            if count_:
                count = count_[0]
            else:
                count = ''
            event_time_ = data.xpath('.//span[@class="lab-time"]/text()')  # 比赛时间
            if event_time_:
                event_time = date + event_time_[0]
            else:
                event_time = ''
            team_home_ = data.xpath('.//span[@class="lab-team-home"]/span/a/text()')  # 主场球队
            if team_home_:
                team_home = team_home_[0]
            else:
                team_home = ''
            team_home_ID_ = data.xpath('.//span[@class="lab-team-home"]/span/a/@href')  # 主场球队ID
            if team_home_ID_:
                team_home_ID = team_home_ID_[0].split('-')[-1]
            else:
                team_home_ID = ''
            score_ = data.xpath('.//span[@class="score"]/span/text()')  # 比分
            if score_:
                score = score_[0]
            else:
                score = ''
            team_away_ = data.xpath('.//span[@class="lab-team-away"]/span/a/text()')  # 客场球队
            if team_away_:
                team_away = team_away_[0]
            else:
                team_away = ''
            team_away_ID_ = data.xpath('.//span[@class="lab-team-away"]/span/a/@href')  # 客场球队ID
            if team_away_ID_:
                team_away_ID = team_away_ID_[0].split('-')[-1]
            else:
                team_away_ID = ''
            lab_ratel_ = data.xpath('.//span[@class="lab-ratel"]/text()')  # 让球
            if lab_ratel_:
                lab_ratel = lab_ratel_[0]
            else:
                lab_ratel = ''
            dic = {'赛事ID': event_ID, '赛事LOGO': event_LOGO, '赛事': event, '轮次': count, '比赛时间': event_time, '主场球队': team_home,
                           '主场球队ID': team_home_ID, '比分': score, '客场球队': team_away, '客场球队ID': team_away_ID,
                           '让球': lab_ratel}
            # 保存数据库
            self.mongo.insert_one(dic, '赛事ID')
            self.redis.insert_one('football_future_events', event_ID, event_ID)

    def run(self):
        # 储存线程的列表
        threads = []
        for i in range(-3, 6):
            if i != 0:
                thread = threading.Thread(target=self.get_response, args=(i, ))
                threads.append(thread)
                # 启动线程
                thread.start()
            else:
                continue
        # 守护线程
        for thread in threads:
            thread.join()
        # self.get_response(6)

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
    # timedata = TimeDataSpider()
    # timedata.get_response(-1)
    TimeDataSpider.start()