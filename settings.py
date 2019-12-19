# 请求头信息
HEADERS={
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.8',
    'cache-control':'no-cache',
    'cookie':'_iuqxldmzr_=32; _ntes_nnid=6c25da66a774146f6e2e7dba7c438195,1570148062671; _ntes_nuid=6c25da66a774146f6e2e7dba7c438195; WM_TID=kUOiXFEdatlFBBAUEFZ9pod0F6gD5MKX; WM_NI=cGhFrl1EZzIfwaiFJAw%2FP7vT8XNcFGmawRWhUt5XkQKgIvDoeNwXeq%2FT6lfIbDn0WcSL9RqICki2QImzMrrf1z%2BLqg8tkozkVgzqFb5PFnkfiUcPd%2BbpK4jCgnYWmmDDMnA%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee96d540bb8aa4a8f646f3b48fa2c45a869a8ebab77b948dfad1cb7a96ee97b7c22af0fea7c3b92aa199a8a7f168f39b969bcc6eb5bfa7a7c94bb5f1a0d8f560fc888284c54dafbfb9b3d66497acfbb9ea5b89b98797c765a792b9b9e87bed8cfa8de543a29ca2d1d6699194f7b3f44381b5a7d3d443afa68393f16ef3a6e5adf46dfcaca590f96196b9b692c56af7908a8fea6eab8badb1e721a2b085d5e949a5b297b8f067889c838fc437e2a3; playerid=30800114; JSESSIONID-WYYY=TZ5sugQdMdDqGMRmpx8us%2Fwm1CB%5C53i0w%5CVBPA%2F7SRcV47c9%5CpesqyDNj%5CKKudONyOBBStSdbCgFowgRyuF27M8N%5Cyy6BN4%2BG73xl4y2HPacrvmj52YTylMSBvSHeV%2FjeHx7g7UXJocpm6b5bblbf7uM5vHPp5NM3KXukZO7ZYwnt3uY%3A1575482951719',
    'pragma':'no-cache',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'
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
