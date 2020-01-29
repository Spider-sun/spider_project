from pymongo import MongoClient

from basketball.settings import MONGO_URL


class MongoDB(object):
    def __init__(self, kind, type='football'):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.mongo = self.client[type][kind]

    def insert_one(self, dic, _id):
        '''实现插入功能'''
        # 判断是否已经存在
        count = self.mongo.count_documents({'_id': dic[_id]})
        # 若不存在
        if count == 0:
            # 使用MongoDB数据库的主键：_id
            dic['_id'] = dic[_id]
            # 插入内容
            self.mongo.insert_one(dic)
            print(f'插入内容：{dic}')
        # 若在数据库中已存在
        else:
            self.update_one(dic, _id)

    def update_one(self, dic, _id):
        '''实现修改功能'''
        # 更新数据
        self.mongo.update_one({'_id': dic[_id]}, {'$set': dic})
        print(f'更新数据{dic}')

    def delete_one(self, id):
        '''实现删除功能'''
        self.mongo.delete_one({'_id': id})
        # 写入日志
        print(f'删除过期数据：{id}')

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
            music_list.append(item)
        return music_list