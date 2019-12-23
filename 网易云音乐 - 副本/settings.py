# 请求头信息
HEADERS={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8',
    'cache-control': 'no-cache',
    'cookie': '_iuqxldmzr_=32; _ntes_nnid=6c25da66a774146f6e2e7dba7c438195,1570148062671; _ntes_nuid=6c25da66a774146f6e2e7dba7c438195; WM_TID=kUOiXFEdatlFBBAUEFZ9pod0F6gD5MKX; JSESSIONID-WYYY=B7iVu5zikAt%5CnBK9Y9QEFksTWM9aZ1i3ZxVe%2FJuy6IhYeHRmXIDOVuMhCAdmq%2B9k%2FeYFJrEiQXxDPaYsAAqB5IJjNMuCBpZksqEMZ4PuCSVx57kfn61KMZXuJ3h3Io9YC4bDrcBvojwY0hOSovd%5CWVIeyOl6a1XBs08R95%5C7MkZadYP1%3A1577077509508; WM_NI=Mnlr2TQ7V8C3PNzlfHGa7mvolEMhBXvKi6MRJjQTtGe2hu4NpqGPNy0W2p%2F2aviYut0uIHyTFWVwJJK62hcCKnKG%2Bbr6pYAXOlSbY2MOhDg3%2FGzElXgU9v1YtMpIp%2BGvUXM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed8b75d838e8f95e280b5e78ea3d85b978f8faeee7ba9e888a3d96a8194fd98d22af0fea7c3b92a8fb2a493b16093e99ad9c2399492b68de54485bff98ef565b09b8389c154b695a7d7d05a8ab69fb5f74da7eea896b746b4af89b1cd73f489fe91ae3aa3aaa7baf880f4ab87a9fc6086899a98c94289eafe89e24989b285a8aa6ab2eac0bac4548db49d83dc3a8f91a8a5e639ed99b6a6ef54a58bf797b453b893c0aaf32185aa9bb9d037e2a3',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'
}

# MongoDB数据库的URL
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 做可视化信息的歌曲数量
VISUAL_MUSIC_NUMBER = 10

# 做可视化信息的热评数量
VISUAL_COMMENTS_NUMBER = 5

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                                      # 可视化饼图配置信息
# 控制饼图为正圆
ASPECT = 'equal'
# 绘图形状
KIND = 'pie'
# 饼图中添加数值标签
AUTOPCT = '%.1f%%'
# 设置饼图的半径
RADIUS = 1
# 设置饼图的初始角度
STARTANGLE = 180
# 将饼图的顺序设置为顺时针方向
COUNTERCLOCK = False
# 设置饼图内外边界属性值
WEDGEPROPS={'linewidth': 1.5, 'edgecolor': 'green'}
# 设置文本标签属性值
TEXTPROPS={'fontsize': 10, 'color': 'black'}
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
