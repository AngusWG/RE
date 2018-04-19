#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
from bin.crawler import Crawler
from bin.db_utils import DBUtils
from bin.log import log


class Server:
    """接受来自界面的各种请求"""

    def __init__(self, log: log):
        self.max_num = 100
        self.log = log
        self.crawler = Crawler(self.log)
        self.db = DBUtils()
        self.log.info("数据库载入成功")
        self.log.info("服务载入成功")

    def film_name_list(self, char=""):
        """快速检查用"""
        return self.crawler.file_name_list(char)

    def same_attributes(self, *args):
        """基于相同属性的推荐电影"""
        # 获得电影标签
        args = [self.film_info(i) for i in args]
        tags = []
        # same_tags = self.calc_same_tag(*[i.get("tags") for i in args])
        [tags.extend(i.get("tags")) for i in args]
        print(tags)
        # 查询有相同标签的电影
        file_list = [self.find_films_by_tag(i) for i in tags]
        # 分析推荐电影

    def same_taste(self, *args):
        """基于相同品味的推荐电影"""
        # 获取热爱这个电影的用户id

        # 查询每个用户喜欢的其他电影

        # 计算权重最高

        pass

    def film_info(self, id):
        """获得电影信息"""
        return self.db.file_info_by_id(id) or self.db.save_file(self.crawler.film_info_by_id(id))

    def user_info(self, id):
        """获得用户信息"""
        return self.db.user_info_by_id(id) or self.db.save_user(self.crawler.user_info(id))

    @staticmethod
    def calc_same_tag(*arg):
        data = dict()
        list_data = []
        [list_data.extend(i) for i in arg]
        for item in list_data:
            i = data.get(item)
            data[item] = i + 1 if i else 0
        data = dict(filter(lambda x: x[1] != 0, data.items()))
        data = list(sorted(data.items(), key=lambda x: x[1], reverse=True))
        return data[:int(len(data) / 2)] if len(data) > 10 else data

    def find_films_by_tag(self, char):
        db_data = self.db.search(char)
        db_data_id = set([i.get("_id") for i in db_data])
        if len(db_data_id) > self.max_num:
            return db_data
        self.log.info("标签 {} 数据不够，数据库数据量为 {} 开始爬取".format(char, len(db_data_id)))
        crawler_id = set(self.crawler.same_tag_list(char))
        search_id = list(crawler_id - db_data_id)
        # todo 进度条
        search_data = [self.film_info(i) for i in search_id]
        data = search_data + db_data
        self.log.info("{} 数据爬取完毕".format(char))
        return data


def test233():
    server = Server(log())
    res = ["她 Her (2013)", "怦然心动", "小情人", "初恋这件小事", "宝贝老板", "爱宠大机密", "香肠派对", "欢乐好声音", "冰雪奇缘", "无敌破坏王", "疯狂动物城"]
    for i in res:
        res.append(server.film_name_list(i)[0])
    server.same_attributes(*res)


if __name__ == '__main__':
    server = Server(log())
    # file0 = server.film_name_list("无间道")[0]
    # file1 = server.film_name_list("禁闭岛")[0]
    # file2 = server.film_name_list("触不可及")[0]
    # print(file0, file1, file2)
    server.same_attributes("1307914", "1307914", "6786002")
    # a = server.find_films_by_tag("黑帮")

    # print(a)
    # print(len(set([i.get("_id") for i in a])))
    pass
