import time
import schedule

from basketball.db.mongo_pool import MongoDB


"""
    清除过期数据
"""
class Delete_home_page(object):
    def __init__(self):
        self.mongo_home_page = MongoDB('home_page')
        self.mongo_home_info  = MongoDB('home_info ')
        self.mongo_detail = MongoDB('detail')
        self.mongo_shujufenxi = MongoDB('shujufenxi')

    def get_data(self):
        # 过期数据时间
        date = time.strftime('%Y%m%d', time.localtime(time.time() - 4 * 24 * 3600))
        datas = self.mongo_home_page.find(conditions={'时间': '{} {}'.format(date, date[4: 6] + '/' + date[6:])})
        for data in datas:
            ID = data['赛事ID']
            # 删除过期信息
            self.mongo_home_page.delete_one(ID)
            self.mongo_home_info.delete_one(ID)
            self.mongo_detail.delete_one(ID)
            self.mongo_shujufenxi.delete_one(ID)

    def run(self):
        if time.strftime('%H', time.localtime(time.time())) == '00':
            self.get_data()

    @classmethod
    def start(cls):
        st = cls()
        # 每隔一段时间执行一次run方法
        schedule.every(1).hours.do(st.run)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    delete = Delete_home_page()
    delete.get_data()