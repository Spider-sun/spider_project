import requests
import re
import json
import execjs

from core.db.mongo_pool import MongoDB
from settings import HEADERS
from domain import Music


class WangYiYun(object):
    def __init__(self):
        # 实例化对象
        self.mongo = MongoDB()
        # 用于获取歌曲信息的URL
        self.song_url = 'https://music.163.com/discover/toplist?id=3778678'
        # 用于获取评论信息的URL
        self.comment_url = 'https://music.163.com/weapi/v1/resource/comments/{}?csrf_token='

    def get_js_function(self, commentThreadId, page):
        '''
        获取指定目录下的js代码, 并且指定js代码中函数的名字以及函数的参数。
        :param js_path: js代码的位置
        :param func_name: js代码中函数的名字
        :param func_args: js代码中函数的参数
        :return: 返回调用js函数的结果
        '''
        with open(r'C:\Users\me\Desktop\网易云音乐 - 副本\crack\crack.js', encoding='utf-8') as fp:
            js = fp.read()
            ctx = execjs.compile(js)
            return ctx.call('d', commentThreadId, page)

    def get_song_info(self):
        # 获取网页源代码
        response = requests.get(self.song_url, headers=HEADERS).text
        # 正则表达式筛选出歌曲信息
        result = re.findall('>(\[.*?\])<', response)[0]
        # 将数据信息转为JSON格式
        songs_info_json = json.loads(result)
        # 提取信息列表
        for i in range(len(songs_info_json)):
            # 获取歌曲ID
            id = songs_info_json[i]['id']
            # 获取歌曲名
            sing_name = songs_info_json[i]['name']
            # 获取歌手名
            singer_name = songs_info_json[i]['artists'][0]['name']
            # 获取专辑名
            special_name = songs_info_json[i]['album']['name']
            # 获取歌曲评论的ID
            commentThreadId = songs_info_json[i]['commentThreadId']
            # 获取评论信息
            hotComments = self.get_comments(commentThreadId)
            # 获取歌曲排名
            rank = i + 1
            # 整合数据的字典
            music = {'id': id, 'sing_name': sing_name, 'singer_name':singer_name, 'special_name': special_name, 'hotComments': hotComments, 'rank': rank}
            music = Music(**music)
            # 保存数据
            self.mongo.insert_one(music)

    def get_comments(self, commentThreadId):
        params_dict = self.get_js_function(commentThreadId, 0)
        params = {
            'params': params_dict['encText'],
            'encSecKey': params_dict['encSecKey']
        }
        # 获取评论信息
        response = requests.post('https://music.163.com/weapi/v1/resource/comments/' + commentThreadId + '?csrf_token=', headers=HEADERS, params=params).text
        print(response)
        # 将信息转为JSON格式
        hotComments = json.loads(response)['hotComments']
        # 提取热评，并返回数据
        hotComments_ls = []
        for comment in self.get_comments_data(hotComments):
            hotComments_ls.append(comment)
        # 将获取的评论数据返回
        return hotComments_ls

    def get_comments_data(self, hotComments):
        '''获取评论信息'''
        for hotComment in hotComments:
            # 获取评论者名字
            nickname = hotComment['user']['nickname']
            # 获取评论信息
            content = hotComment['content']
            # 获取点赞数
            likedCount = hotComment['likedCount']
            # 将数据格式化
            dic = {'nickname': nickname, 'content': content, 'likedCount': likedCount}
            # 返回字典数据
            yield dic

    # 装饰器把实例方法改为类方法，可由类对象直接调用
    @classmethod
    def start(cls):
        # 实例化对象
        wangyiyun = cls()
        # 调用方法
        wangyiyun.get_song_info()


if __name__ == '__main__':
    # wangyiyun = WangYiYun()
    # wangyiyun.get_js_function()
    WangYiYun.start()
