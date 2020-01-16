from settings import MAX_SCORE


class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=-1, score=MAX_SCORE, disable_domains=[]):
        '''
        :param ip: 代理的ip地址
        :param port: 代理ip的端口号
        :param protocol: 代理ip支持的协议类型，http是0，https是1，http&https是2
        :param nick_type: 代理的匿名程度， 高匿：0，匿名：1，透明：2
        :param speed: 代理ip的响应速度，单位：s
        :param area: 代理ip所在地区
        :param score: 代理ip的评分
        :param disable_domains: 不可用的ip
        '''
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.nick_type = nick_type
        self.speed = speed
        self.area = area
        self.score = score
        self.disable_domains = disable_domains

    # 提供 _str_ 方法， 返回的数字字符串
    def __str__(self):
        # 返回数字字符串
        return str(self.__dict__)
