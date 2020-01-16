import requests
import random
import schedule
import time

from IP_API.db.redis_pool import Redis_Pool
redis = Redis_Pool()


# 设置代理
def get_ip():
    try:
        proxies = redis.find('proxy_')
        keys = []
        for key in proxies.keys():
            keys.append(key.decode('utf-8'))
        proxy = random.choice(keys)
    except:
        proxy = ''
    # 把需要用的代理返回
    return proxy


def get_proxy():
    def start():
        redis.delete('proxy_')
        proxies = requests.get('http://dps.kdlapi.com/api/getdps/?orderid=957415078493226&num=100&pt=1&sep=1').text.split()
        can()
        for proxy in proxies:
            redis.insert_one('proxy_', proxy, proxy)

    start()
    schedule.every(10).seconds.do(start)
    while True:
        schedule.run_pending()
        time.sleep(1)


# 快代理设置白名单
def can():
    api_url = "https://dev.kdlapi.com/api/setipwhitelist"
    data = {
        'orderid': 'xxxxxxxxxxxx',
        'iplist': 'xxx.xxx.xxx.xxx, xxx.xxx.xxx.xxx',  # 需要设置的白名单
        'signature': 'xxxxxxxxxxxxxxxxxxxxx',
    }
    r = requests.post(url=api_url, data=data)
    # print(r.status_code)  # 获取Reponse的返回码
    # print(r.content.decode('utf-8'))  # 获取页面内容

