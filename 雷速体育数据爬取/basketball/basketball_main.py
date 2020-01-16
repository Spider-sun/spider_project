from multiprocessing import Process

from basketball.spiders.home_spider import HomeSpider
from basketball.spiders.new_data_spider import NewSpider
from basketball.spiders.data_spider import DataSpider


def run():
    # 定义一个列表，用于储存要启动的进程
    process_list = []
    # 创建启动HomeSpider爬虫的进程
    process_list.append(Process(target=HomeSpider.start))
    # 创建启动NewSpider爬虫的进程
    process_list.append(Process(target=NewSpider.start))
    # 创建启动DataSpider中爬取正在比赛的信息的爬虫的进程
    process_list.append(Process(target=DataSpider.start))
    # 创建启动进程
    for process in process_list:
        # 设置守护进程
        process.daemon = True
        process.start()

    # 遍历列表，让主线程等待子进程完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    HomeSpider().get_home_data()
    run()