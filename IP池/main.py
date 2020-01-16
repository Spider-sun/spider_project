from multiprocessing import Process

from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi


def run():
    # 定义一个列表，用于储存要启动的进程
    process_list = []
    # 创建启动爬虫的进程
    process_list.append(Process(target=RunSpider.start))
    # 创建启动检测的进程
    process_list.append(Process(target=ProxyTester.start))
    # 创建启动提供API服务的进程
    process_list.append(Process(target=ProxyApi.start))

    # 遍历进程列表，启动所有进程
    for process in process_list:
        # 设置守护进程
        process.daemon = True
        process.start()

    # 遍历列表，让主线程等待子进程完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()