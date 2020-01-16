from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
import time

from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL


class ProxyTester(object):

    def __init__(self):
        # 创建操作数据库的MongoPool对象
        self.mongo_pool = MongoPool()
        # 创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __chech_callbake(self, temp):
        self.coroutine_pool.apply_async(self.__chech_one_proxy, callback=self.__chech_callbake)

    def run(self):
        # 提供一个run方法，用于处理检测代理IP的核心逻辑
        # 1. 从数据库里面获取所有IP
        proxies = self.mongo_pool.find_all()
        # 2. 遍历代理IP列表
        for proxy in proxies:
            # 把代理IP添加到队列里去
            self.queue.put(proxy)

        for i in range(TEST_PROXIES_ASYNC_COUNT):
            # 通过异步回调，使用死循环不断执行这个方法
            self.coroutine_pool.apply_async(self.__chech_one_proxy, callback=self.__chech_callbake)
        # 守护线程
        self.queue.join()

    def __chech_one_proxy(self):
        # 从队列中获取代理IP，进行检查
        proxy = self.queue.get()
        # 3. 检测代理可用性
        proxy = check_proxy(proxy)
        # 4. 如果代理不可用，让代理分数-1
        if proxy.speed == -1:
            proxy.score -= 1
            # 5. 如果代理分数等于0，就从数据库中删除该IP
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                # 6. 否则更新该IP
                self.mongo_pool.update_one(proxy)
        else:
            # 如果代理可用，就恢复该代理分数，更新到数据库中
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        # 调度队列的tesk_done方法
        self.queue.task_done()

    @classmethod
    def start(cls):
        # 创建本类对象
        proxy_tester = cls()
        # 调用run方法
        proxy_tester.run()

        # 每隔一段时间执行一次run方法
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(proxy_tester.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # pt = ProxyTester()
    # pt.run()
    ProxyTester.start()
