
class Music(object):
    def __init__(self, id=None, sing_name=None, singer_name=None, special_name=None, hotComments=None, rank=None):
        '''
        :param id: 歌曲id
        :param sing_name: 歌曲名字
        :param singer_name: 歌手
        :param special_name: 所属专辑
        :param hotComments: 热评
        :param rank: 歌曲排名
        '''
        self.id = id
        self.sing_name = sing_name
        self.singer_name = singer_name
        self.special_name = special_name
        self.hotComments = hotComments
        self.rank = rank

    # 提供 __str__ 方法， 返回字符串
    def __str__(self):
        # 返回数字字符串
        return str(self.__dict__)