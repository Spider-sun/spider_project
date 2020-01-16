import importlib
import threading
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

from settings import PROXIES_SPIDER
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger


class RunSpider(object):
    def __init__(self):
        # 创建MongoPool对象
        self.mongo_pool = MongoPool()
        # 创建协程池对象
        self.coroutine_pool = Pool()

    def get_spider_from_settings(self):
        # 根据配置文件信息，获取爬虫对象列表
        for full_class_name in PROXIES_SPIDER:
            #'core/proxy_spider/proxy_spiders/XiCiSpiderpy'
            # 获取模块名 和 类名
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            # 根据模块名，导入模块
            module = importlib.import_module(module_name)
            # 根据类名，从模块中获取类
            cls = getattr(module, class_name)
            spider = cls()
            yield spider

    def run(self):
        # 根据配置文件信息， 获取爬虫对象列表
        spiders = self.get_spider_from_settings()
        # threads = []
        for spider in spiders:
        #     thread = threading.Thread(target=self._execute_one_spider_task, args=(spider,))
        #     threads.append(thread)
        #     thread.start()
        # for thread in threads:
        #     thread.join()
            # self._execute_one_spider_task(spider)
            # 使用异步的方式调用
            self.coroutine_pool.apply_async(self._execute_one_spider_task, args=(spider,))
        # 守护线程
        self.coroutine_pool.join()

    def _execute_one_spider_task(self, spider):
        # 处理一个爬虫任务
        try:
            # 遍历爬虫对象的get_proxies方法，获取代理IP
            for proxy in spider.get_proxies():
                # self.__dispose_one(proxy)
                self.coroutine_pool.apply_async(self.__dispose_one, args=(proxy,))
            # 守护线程
            self.coroutine_pool.join()
        except Exception as e:
            logger.exception(e)

    def __dispose_one(self, proxy):
        # 检测代理IP的可用性
        proxy = check_proxy(proxy)
        # 如果可用，写入数据库
        if proxy.speed != -1:
            # 可用，写入数据库
            self.mongo_pool.insert_one(proxy)

    @classmethod
    def start(cls):
        rs = cls()
        rs.run()


if __name__ == '__main__':
    rs = RunSpider()
    rs.run()