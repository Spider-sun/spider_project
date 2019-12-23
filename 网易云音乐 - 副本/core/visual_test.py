import matplotlib.pyplot as plt
import pandas as pd

from core.music.comments import Comments
from settings import KIND, AUTOPCT, RADIUS, STARTANGLE, COUNTERCLOCK, TEXTPROPS, WEDGEPROPS, ASPECT


class Visual(object):
    def __init__(self):
        # 实例化对象
        self.comments = Comments()

    def get_comments(self):
        # 获取评论信息
        comments = self.comments.get_comments_data()
        # 遍历歌曲列表，获取歌曲下的评论数据
        for comment_data in comments:
            # 拆包、获取歌名及评论
            sing_name, comment_ls = comment_data
            # 建立组合的空字典
            comment_data = {}
            # 遍历评论列表，获取评论信息
            for comment in comment_ls:
                # 添加字典数据
                comment_data[comment[0]] = comment[1]

            # # 调用、绘图
            self.visual_date(sing_name, comment_data)

    def visual_date(self, sing_name, comment_data):
        # 构建序列
        data1 = pd.Series(comment_data)
        # 将序列名称设为空符
        data1.name = ''
        # 控制饼图为正圆
        plt.axes(aspect=ASPECT)
        # plot方法对序列进行绘图
        data1.plot(
            kind=KIND,  # 绘图形状
            autopct=AUTOPCT,  # 饼图中添加数值标签
            radius=RADIUS,  # 设置饼图的半径
            startangle=STARTANGLE,  # 设置饼图的初始角度
            counterclock=COUNTERCLOCK,  # 将饼图的顺序设置为顺时针方向
            title=f'《{sing_name}》',  # 为饼图添加标题
            wedgeprops=WEDGEPROPS,  # 设置饼图内外边界属性值
            textprops=TEXTPROPS  # 设置文本标签属性值
            )
        # 显示中文标签
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 显示图形
        plt.show()

    @classmethod
    def start(cls):
        visual = cls()
        visual.get_comments()


if __name__ == '__main__':
    # v = Visual()
    # v.get_comments()
    Visual.start()