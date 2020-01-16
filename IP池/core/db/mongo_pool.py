from pymongo import MongoClient
from settings import MONGO_URL
from utils.log import logger
from donmain import Proxy
import pymongo
import random
'''
1. 插入数据的方法
2. 修改数据的方法
3. 删除数据的方法
4. 查询所有代理IP的方法
5. 按条件取出IP的方法
6. 根据协议类型 和 要访问的网站域名，获取代理IP列表的方法
7. 随机取出一个IP的方法
8. 把指定域名添加到指定IP的disable_domain列表中
'''


class MongoPool(object):
    def __init__(self):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxy']

    def __del__(self):
        # 关闭数据库的连接
        self.client.close()

    def insert_one(self, proxy):
        '''实现插入功能'''
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 我们使用proxy.ip作为MongoDB中的数据主键：_id
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info(f"插入新代理: {proxy}")
        else:
            logger.warning(f"已存在的代理: {proxy}")

    def update_one(self, proxy):
        '''实现修改功能'''
        self.proxies.update_one({'id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        '''实现删除功能'''
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info(f"删除代理IP: {proxy}")

    def find_all(self):
        '''实现查询所有代理IP的功能'''
        cursor = self.proxies.find()
        for item in cursor:
            # 删除 '_id'这个key
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        '''
        :param conditions: 查询条件字典
        :param count: 限制最多取出多少IP
        :return: 返回满足要求的代理IP(Proxy对象)列表
        '''
        cursor = self.proxies.find(conditions, limit=count).sort([('score',pymongo.DESCENDING),('speed', pymongo.ASCENDING)])
        # 准备列表，用于储存查询处理代理IP
        proxy_list = []
        # 遍历 cursor
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol, domain, count=0, nick_type=0):
        '''
        实现根据协议类型 和 要访问的网站域名，获取代理IP列表
        :param protocol: 协议，http,https
        :param domain: 域名，例： jd.com
        :param count: 用于限制获取多个代理IP，默认获取所有的
        :param nick_type: 匿名类型， 默认，获取高匿代理IP
        :return: 满足要求代理IP
        '''
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议，制定查询条件
        if protocol is None:
            # 如果没有传入协议类型，返回支持http和https的代理IP
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}

        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}

        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
         '''
         实现把指定域名添加到指定IP的disable_domain列表中
         :param ip: IP地址
         :param domain: 域名
         :return: 如果返回True, 就表示添加成功了，否则就失败了
         '''
         if self.proxies.count_documents({'_id':ip, 'disable_domain':domain}) == 0:
            self.proxies.update_one({'_id':ip}, {'$push':{'disable_domains':domain}})


if __name__ == '__main__':
    mongo = MongoPool()
    # for proxy in mongo.find_all():
    print(mongo.get_proxies(None, None, count=5, nick_type=2))
