from core.music.wangyiyun_spider import WangYiYun
from core.visual_test import Visual


def run():
    # 启动网易云爬虫、获取歌曲信息
    WangYiYun.start()
    # 启动绘图
    Visual.start()


if __name__ == '__main__':
    run()