import redis


class Redis_Pool(object):
    def __init__(self):
        # 连接数据库
        self.reids_pool = redis.Redis(host='127.0.0.1', port=6379)

    def insert_one(self, name, key, value):
        '''实现插入功能'''
        self.reids_pool.hset(name, key, value)
        print(f'插入缓存数据{value}')

    def delete(self, name):
        '''实现删除功能'''
        self.reids_pool.delete(name)

    def find(self, name):
        '''实现查询功能'''
        return self.reids_pool.hgetall(name)


if __name__ == '__main__':
    m = Redis_Pool()
    m.insert_one('live', 1, 2)
    m.delete('live')