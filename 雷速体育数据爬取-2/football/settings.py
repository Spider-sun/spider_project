# MONGODB数据库连接
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 请求头
import random
USER_AGENTS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/4.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11.0.1245.0 Safari/537.36",
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0',
    'Mozilla/5.0 (Windows; U; ; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.1a2) Gecko/20060512 BonEcho/2.0a2',
    'Mozilla / 5.0（Macintosh; U; Intel Mac OS X 10.8; it; rv：1.93.26.2658）Gecko / 20141026 Camino / 2.176.223（MultiLang）（例如Firefox / 3.64.2268）0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
]

HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'modeZoneSport1=0; _uab_collina=157872482265634995577197; acw_tc=76b20fe815791841594365190e4e598e8b7821b57f99510f4a8d279f7c3fff; lang=; Hm_lvt_63b82ac6d9948bad5e14b1398610939a=1579154886,1579184161,1579336265,1579528336; acw_sc__=5e281aa276d52c2a1e6ec926bf380259b663e68d; SERVERID=8ee94c93114d0310082f476ad04f1141|1579686562|1579686562; Hm_lpvt_63b82ac6d9948bad5e14b1398610939a=1579686563',
    'Host':'live.leisu.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': random.choice(USER_AGENTS_LIST)
}

# 配置查询历史交锋、近期战绩、联赛积分等数据的时间间隔, 单位是小时
TEST_EVENTS_INTERVAL = 1

# 配置数据分析的异步数量
TEST_PROXIES_ASYNC_COUNT = 500

# 球队三合一数据抓取的时间间隔, 单位秒
TEST_NOTLIVE_INTERVAL = 10

# 主页全部数据刷新的异步数
TEST_HOME_ASYNC_COUNT = 100

# 三合一数据抓取异步数量
TEST_INDEX_DATA = 100
