#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
from pprint import pprint

from bin.crawler import Crawler
from bin.data_analysis import DataAnalysis
from bin.db_utils import DBUtils
from bin.log import log


class Server:
    """接受来自界面的各种请求"""

    def __init__(self, log: log):
        self.film_max = 100
        self.user_max = self.film_max * 1
        self.log = log
        self.crawler = Crawler(film_max=self.film_max, user_max=self.user_max, log=self.log)
        self.db = DBUtils()
        self.log.info("数据库载入成功")
        self.log.info("服务载入成功")
        self.data_analysis = DataAnalysis()

    def film_name_list(self, char=""):
        """快速检查用"""
        return self.crawler.file_name_list(char)

    def same_attributes(self, *args):
        """基于相同属性的推荐电影"""
        # 获得电影标签
        self.log.info("开始电影同标签推荐")
        args = [self.film_info(i) for i in args]
        tags = []
        # same_tags = self.calc_same_tag(*[i.get("tags") for i in args])
        [tags.extend(i.get("tags")) for i in args]
        # 查询有相同标签的电影
        file_list = []
        for n, i in enumerate(tags):
            file_list.extend(self.find_films_by_tag(i))
            self.log.info("开始获取标签 {} 数据".format(i), lev1=n / len(tags))

        # 数据去重
        file_list = [eval(i) for i in set([str(i) for i in file_list])]
        # 去参数
        for i in args:
            file_list.remove(self.film_info(i["_id"]))
        return self.data_analysis.feature_extraction(tags, file_list)

    def same_taste(self, *args):
        """基于相同品味的推荐电影"""
        user_list = []
        for id in args:
            a = self.film_reviews_list(id)['reviews']
            user_list += a
        # 去重
        user_list = list(set(user_list))
        self.log.info(msg="总共需要爬 {} 个用户数据".format(len(user_list)))
        # 获得这类人喜欢的电影
        user_data = []
        for id in user_list:
            user = self.user_info(id)
            user_data += user["films"]
            self.log.info(msg="爬取数据进度 {}%".format(int(user_list.index(id) / len(user_list) * 100)))
        # 去掉参数电影
        self.log.info(msg="共 {} 个电影数据".format(len(user_data)))
        # 计算权重
        rank_data = self.data_analysis.item_collaboration_filter(user_data)
        res = []
        for k, v in rank_data:
            film = self.film_info(k)
            if film['_id'] in args:
                continue
            film["rank"] = v
            res.append(film)
        return res

    def film_info(self, id, tag=None):
        """获得电影信息"""
        if tag:
            data = self.db.file_info_by_id(id) or self.crawler.film_info_by_id(id)
            if tag not in data.get("tags"):
                data["tags"].append(tag)
                return self.db.save_file(data)
        return self.db.file_info_by_id(id) or self.db.save_file(self.crawler.film_info_by_id(id))

    def user_info(self, id):
        """获得用户信息"""
        return self.db.user_info_by_id(id) or self.db.save_user(self.crawler.user_info(id))

    @staticmethod
    def calc_same_tag(*arg):
        data = dict()
        list_data = []
        [list_data.extend(i) for i in arg]
        print(list_data)
        for item in list_data:
            i = data.get(item)
            data[item] = i + 1 if i else 0
        # 去除单个标签
        data = dict(filter(lambda x: x[1] != 0, data.items()))
        # 排序
        data = list(sorted(data.items(), key=lambda x: x[1], reverse=True))
        # 返回前十的标签
        return data[:10] if len(data) > 10 else data

    def find_films_by_tag(self, char):
        db_data = self.db.find_same_tag_film(char)
        db_data_id = set([i.get("_id") for i in db_data])
        if len(db_data_id) > self.film_max:
            self.log.info("标签 {} 从数据库获取到 {} 条 不爬取资源".format(char, len(db_data_id)))
            return db_data
        if self.db.find_tag_file_num(char) < self.film_max:
            return db_data
        self.log.info("标签 {} 数据不够，数据库数据量为 {} 开始爬取".format(char, len(db_data_id)))
        crawler_id = set(self.crawler.same_tag_list(char))
        search_id = list(crawler_id - db_data_id)
        search_data = []
        for n, i in enumerate(search_id):
            self.film_info(i, char)
            self.log.info(msg="正在获取电影数据", lev2=n / len(search_id))
        data = search_data + db_data
        self.log.info("{} 数据爬取完毕".format(char))
        self.db.save_tag_file_num(char, len(search_id))
        return data

    def save_data(self, file_list):
        with open("data.txt", "w+", encoding="utf8") as f:
            for item in file_list:
                tag_list = [i + " " for i in item.get("tags")]

                print(item.get("_id"), tag_list)
                data = item.get("_id") + "\t" + "".join(tag_list)
                f.write(data + "\n")

    def film_reviews_list(self, id):
        film = self.db.find_file_reviews_by_id(id)
        # if not film or len(film.get("reviews")) < self.user_max - 5:
        if film is None:
            self.log.info("{}数据不够。从网络爬取".format(id))
            reviews = self.crawler.film_review_list(id)
            film = self.db.save_film_reviews({"_id": id, "reviews": reviews})
        return film


if __name__ == '__main__':
    pass
