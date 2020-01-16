import requests
import re
import json
import time
import schedule

from football.db.mongo_pool import MongoDB
from football.db.redis_pool import Redis_Pool
from IP_API.proxy import get_ip
from football.settings import HEADERS


class RedisID(object):
    def __init__(self):
        # 建立数据库连接
        self.mongo = MongoDB('home_page')
        self.redis = Redis_Pool()
        # 主页 URL
        self.url = 'https://live.leisu.com/'

    def get_data(self):
        # 发起请求 获取网页源代码
        try:
            proxy = get_ip()
            if proxy:
                response = requests.get(self.url, headers=HEADERS, proxies = {'https': 'https://'+proxy}, allow_redirects=False, timeout=3).text
            else:
                response = requests.get(self.url, headers=HEADERS, allow_redirects=False).text
            # 正则获取 js 数据
            result = re.findall('THATDATA=(.*})', response)

            # 转 JSON 格式
            data = json.loads(result[1])
            # 球队信息
            teams = data['teams']
            # 赛事
            events = data['events']
            # 正在比赛的信息
            live = data['matchesTrans']['live']
            self._dispose_live('football_live', events, live, teams)

            # 未开始的比赛
            notStart = data['matchesTrans']['notStart']
            self._dispose_live('football_notStart', events, notStart, teams)

            # 已完成的比赛
            finished = data['matchesTrans']['finished']
            self._dispose_live('football_finished', events, finished, teams)

            # 其他
            other = data['matchesTrans']['other']
            self._dispose_live('football_other', events, other, teams)
        except:
            pass

    def _dispose_live(self, name, events, type, teams):
        '''处理正在比赛的球队'''
        self.redis.delete(name)
        for li in type:
            d = {}
            events_ID = li[0]  # 赛事ID
            event = events[str(li[1])][0].split(',')[0]  # 赛事
            event_LOGO = 'https://cdn.leisu.com/eventlogo/' + events[str(li[1])][-2]  # 赛事LOGO
            start_time = time.strftime('%H:%M', time.localtime(li[3]))  # 时间
            zhuangtai = (time.time() - li[3]) / 60 - 20  # 状态
            home_team = teams[str(li[5][0])][0].split(',')[0]  # 主场球队
            home_team_ID = li[5][0]  # 主场球队ID
            away_team = teams[str(li[6][0])][0].split(',')[0]  # 客场球队
            away_team_ID = li[6][0]  # 客场球队ID
            d['赛事ID'] = events_ID
            d['赛事'] = event
            d['赛事LOGO'] = event_LOGO
            d['时间'] = start_time
            d['状态'] = int(zhuangtai)
            d['主场球队'] = home_team
            d['主场球队ID'] = home_team_ID
            d['客场球队'] = away_team
            d['客场球队ID'] = away_team_ID

            self.redis.insert_one(name, events_ID, d.__str__())

    @classmethod
    def start(cls):
        run = cls()
        while True:
            try:
                run.get_data()
            except requests.exceptions.ProxyError:
                pass


if __name__ == '__main__':
    # home = RedisID()
    # while True:
    #     try:
    #         home.get_data()
    #     except:
    #         pass
    # # time.sleep(1)
    RedisID.start()