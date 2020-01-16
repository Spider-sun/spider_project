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
    'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
    'Mozilla/5.0 (Windows; U; ; en-EN) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.8.0'
]

HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'acw_tc=76b20ff615786434667988016e322a3575a5708b1f4a70c89a3936e2d60c30; modeZoneSport1=0; _uab_collina=157872482265634995577197; Hm_lvt_63b82ac6d9948bad5e14b1398610939a=1578890423,1578912776,1578943839,1578995384; acw_sc__=5e1df403c001164fd7444ec975b095a104f46ac3; SERVERID=4ab2f7c19b72630dd03ede01228e3e61|1579021316|1579021316; Hm_lpvt_63b82ac6d9948bad5e14b1398610939a=1579021317',
    'Host':'live.leisu.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': random.choice(USER_AGENTS_LIST)
}

# 历史数据等信息，开启的多线程数量
DATA_THREADING = 5

# 历史数据、未来赛程等数据的爬取时间间隔，单位秒
DATA_LIVE_TIME = 300

# 文字直播线程数
NEW_THREADING = 5