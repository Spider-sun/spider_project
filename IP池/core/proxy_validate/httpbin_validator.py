import time
import json
import requests
from utils import http
from settings import TEST_TIMEOUT
from donmain import Proxy


def check_proxy(proxy):
    '''
    用于检测指定 代理IP 响应速度， 支持的协议类型
    :param proxy: 代理IP模型对象
    :return:
    '''

    # 准备代理IP字典
    proxies = {
        'http': f'http://{proxy.ip}:{proxy.port}',
        'https': f'https://{proxy.ip}:{proxy.port}'
    }
    # 检测该代理IP
    http, http_nick_type, http_speed = _check_http_proxies(proxies)
    https, https_nick_type, https_speed = _check_http_proxies(proxies, False)

    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


def _check_http_proxies(proxies, is_http=True):
    nick_type = -1  # 匿名程度
    speed = -1

    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'

    # 获取开始时间
    start = time.time()
    try:
        # 发送请求
        response = requests.get(test_url, headers=http.get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)

        if response.ok:
            speed = round(time.time()-start, 2)
            # 匿名程度
            # 把响应的JSON字符串转为字典
            dic = json.loads(response.text)
            # 获取来源的IP：origin
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            if ',' in origin:
                # 如果响应的origin中有','分割的两个IP就是透明代理IP
                nick_type = 2
            elif proxy_connection:
                # 如果响应的headers中包含Proxy-Connection 说明是匿名代理IP
                nick_type = 1
            else:
                # 否则是高匿
                nick_type = 0

            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        return False, nick_type, speed

