
# 定义 MAX_SCORE 表示代理IP的默认最高分
MAX_SCORE = 5

# 日志配置信息
import logging
LOG_LEVEL = logging.DEBUG  # 默认等级
LOG_FMT = "%(asctime)s - %(filename)s - [line: %(lineno)d] %(levelname)s: %(message)s"
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名

# 测试代理的超时时间
TEST_TIMEOUT = 10

# MongoDB数据库的URL
MONGO_URL = 'mongodb://127.0.0.1:27017'


PROXIES_SPIDER = [
    # 爬虫的全类名，路径，模块，类名
    'core.proxy_spider.proxy_spiders.XiCiSpider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.Ip66Spider'
]


# 配置检测代理IP的异步数量
TEST_PROXIES_ASYNC_COUNT = 100

# 配置检查代理IP的时间间隔, 单位是小时
TEST_PROXIES_INTERVAL = 2

# 配置获取的代理IP的最大数量；这个数越小，可用性越高，但随机性越差
PROXIES_MAX_COUNT = 50