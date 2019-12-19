from pymongo import MongoClient

from settings import MONGO_URL
from domain import Music
from log import logger


class MongoDB(object):
    def __init__(self):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.mongo = self.client['music']['sings']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, music):
        '''实现插入功能'''
        # 判断该歌曲是否已经存在
        count = self.mongo.count_documents({'id': music.id})
        # 若不存在
        if count == 0:
            # 使用music.id为MongoDB数据库的主键：_id
            dic = music.__dict__
            dic['_id'] = music.id
            # 插入内容
            self.mongo.insert_one(dic)
            logger.info(f'插入音乐内容：{music.sing_name}')
        # 若歌曲在数据库中已存在
        else:
            logger.warning(f'已存在音乐内容：{music.sing_name}')

    def update_one(self, music):
        '''实现修改功能'''
        # 更新数据
        self.mongo.update_one({'_id': music.id}, {'$set': music.__dict__})
        # 写入日志
        logger.info(f'修改{music.singer_name}音乐信息为{music}')

    def delete_one(self, music):
        '''实现删除功能'''
        self.mongo.delete_one({'_id': music.id})
        # 写入日志
        logger.info(f'删除歌曲：{music.singer_name}')

    def find(self, conditions={}, count=0):
        '''
        :param conditions: 查询条件的字典
        :param count: 限制查询个数
        :return: 返回满足要求的音乐列表
        '''
        cursor = self.mongo.find(conditions, limit=count)
        # 准备列表，用于储存查询处理音乐
        music_list = []
        # 遍历 cursor
        for item in cursor:
            item.pop('_id')
            music = Music(**item)
            music_list.append(music)
        return music_list
