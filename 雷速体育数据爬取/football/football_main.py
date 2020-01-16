from multiprocessing import Process

from football.RedisID.redis_id_spider import RedisID
from football.spiders.home_spider import HomePage
from football.spiders.data_spider import DataSpider
from football.spiders.index_spider import IndexSpider


def run():
    # 定义一个列表，用于储存要启动的进程
    process_list = []
    # 创建启动RedisID爬虫的进程
    process_list.append(Process(target=RedisID.start))
    # 创建启动home_spider爬虫的进程
    process_list.append(Process(target=HomePage.start))
    # 创建启动data_spider爬虫的进程
    process_list.append(Process(target=DataSpider.start))
    # 创建启动index_spider爬虫的进程
    process_list.append(Process(target=IndexSpider.start))
    # 遍历进程列表，启动所有进程
    for process in process_list:
        # 设置守护进程
        process.daemon = True
        process.start()

    # 遍历列表，让主线程等待子进程完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    RedisID().get_data()
    run()