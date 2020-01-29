import requests
import random
import schedule
import time

from IP_API.db.redis_pool import Redis_Pool
redis = Redis_Pool()


'''
    代理接口
'''
# 设置代理
def get_ip():
    try:
        # 从redis数据库中获取IP
        proxies = redis.find('proxy_')
        keys = []
        for key in proxies.keys():
            keys.append(key.decode('utf-8'))
        proxy = random.choice(keys)
    except:
        proxy = ''
    # 把需要用的代理返回
    return proxy


'''
    以下内容为代理程序
'''
# 快代理接口
def get_proxy():
    def start():
        redis.delete('proxy_')
        proxies = requests.get('http://dps.kdlapi.com/api/getdps/?orderid=957415078493226&num=100&pt=1&sep=1').text.split()
        can()
        for proxy in proxies:
            redis.insert_one('proxy_', proxy, proxy)

    start()
    # 每 60s 刷新一次代理
    schedule.every(10).seconds.do(start)
    while True:
        schedule.run_pending()
        time.sleep(1)


# 快代理设置白名单
def can():
    api_url = "https://dev.kdlapi.com/api/setipwhitelist"
    data = {
        'orderid': '957415078493226',  # 用户的orderid值
        'iplist': '123.163.213.19, 123.163.213.19',  # 需要设置的白名单
        'signature': 'l6l71rism9jh0g3w45ujvyxsp4xcu0f1',  # 用户的Key值
    }
    r = requests.post(url=api_url, data=data)
    # print(r.status_code)  # 获取Reponse的返回码
    # print(r.content.decode('utf-8'))  # 获取页面内容

