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
        tags = []
        [tags.extend(self.film_info(i).get("tags") )for i in args]
        print(tags)
        pass

    def same_taste(self,*args):
        """基于相同品味的推荐电影"""
        pass

    def film_info(self, film_name):
        """获得电影信息"""
        return self.db.file_info_by_name(film_name) or self.db.save_info(self.crawler.film_info_by_name(film_name))
        # return self.crawler.film_info_by_name(film_name)


if __name__ == '__main__':
    server = Server(log())
    file0 = server.film_name_list("无间道")[0]
    file1 = server.film_name_list("禁闭岛")[0]
    file2 = server.film_name_list("触不可及")[0]
    print(file0, file1, file2)
    server.same_attributes(file0, file1, file2)

    # print(server.film_info(file))
