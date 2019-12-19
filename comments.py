mongodb import MongoDB
from settings import VISUAL_COMMENTS_NUMBER, VISUAL_MUSIC_NUMBER


class Comments(object):
    def __init__(self):
        # 实例化对象
        self.mongo = MongoDB()

    def get_comments_data(self):
        '''获取排名下的歌曲信息'''
        for i in range(VISUAL_MUSIC_NUMBER):
            # 获取歌名
            sing_name = self.mongo.find({'rank': i+1})[0].sing_name
            # 获取评论
            comments = self.mongo.find({'rank': i+1})[0].hotComments
            # 提取点赞前五名的评论信息
            # 用于存储数据的空列表
            comments_ls = []
            # 判断自定义的评论长度是否大于原有长度
            if VISUAL_COMMENTS_NUMBER > len(comments):
                lang = len(comments)
            else:
                lang = VISUAL_COMMENTS_NUMBER
            for i in range(lang):
                # 获取评论者姓名
                nickname = comments[i]['nickname']
                # 获取点赞数
                comment_number = comments[i]['likedCount']
                comments_ls.append([nickname, comment_number])
            yield sing_name, comments_ls


if __name__ == '__main__':
    comments = Comments()
    data = comments.get_comments_data()
    for da in data:
        print(da)
        print('-'*50)



