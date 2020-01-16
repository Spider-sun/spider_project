from flask import Flask, request
import json

from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT


class ProxyApi(object):
    def __init__(self):
        # 初始化一个Flask的Web服务
        self.app = Flask(__name__)
        # 创建MongoPool对象，用于操作数据库
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            '''
            根据协议类型和域名，提供随机的获取高可用代理IP的服务
            :protocol: 当前请求的协议类型
            ：domain: 当前请求域名
            '''
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=PROXIES_MAX_COUNT, nick_type=2)

            if protocol:
                return "{}://{}:{}".format(protocol, proxy.ip, proxy.port)
            else:
                return "{}:{}".format(proxy.ip, proxy.port)

        @self.app.route('/proxies')
        def proxies():
            '''
            实现根据协议类型和域名，提供获取多个高可用代理的IP服务
            :return:
            '''
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_MAX_COUNT, nick_type=0)
            # proxies 是一个Proxy对象列表，需要转化为字典列表
            # 转化为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
            # 返回json格式的字符串
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            '''
            如果在获取IP的时候，有指定域名参数，将不再获取该IP，从而进一步提高代理IP的可用性
            :return:
            '''
            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return "请提供ip参数"
            if domain is None:
                return "请提供域名domain参数"

            self.mongo_pool.disable_domain(ip, domain)
            return f"{ip}禁用域名{domain}成功"

    def run(self):
        self.app.run('0.0.0.0', port=16888)

    @classmethod
    def start(cls):
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    ProxyApi.start()
