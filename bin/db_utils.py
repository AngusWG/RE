#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
import socket
import time

import pymongo

from bin.log import log


class DBUtils:
    def __init__(self):
        self.db = self.db_check()
        self.invalid_time = 30 * 24 * 3600

    def valid(self, info):
        """检查数据是否过期"""
        if not info:
            return None
        return info if self.now() > info["time"] else None

    @staticmethod
    def db_check():
        try:
            re = pymongo.MongoClient("www.4yewu.cn", 27017)["RE"]
            re["log"].insert_one(
                {"_id": time.time(), "name": socket.gethostname(), "ip": socket.gethostbyname(socket.gethostname())})
        except pymongo.errors.ServerSelectionTimeoutError as err:
            log().error("无法连接到数据，请通知管理员", err)
            return None
        return re

    @staticmethod
    def now():
        return int(time.time())

    def file_info_by_name(self, film_name):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"name": film_name})
        return self.valid(res)

    def file_info_by_id(self, id):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"_id": id})
        return self.valid(res)

    def user_info_by_id(self, id):
        """获取一部电影的信息"""
        res = self.db["user_info"].find_one({"_id": id})
        return self.valid(res)

    def file_name_list(self, char=""):
        """搜索数据库中电影的名字集，结果多于X条返回None，名字错误返回False，"""
        res = []
        for item in self.db["name_info"].find({"name": {"$regex": ".*" + char + ".*", "$options": "$i"}}):
            res.append(item["name"])
        return self.valid(res)

    def save_file(self, info):
        """存储电影信息"""
        info["time"] = self.now()
        self.db["film_info"].update({"_id": info["_id"]}, {"$set": info}, upsert=True)
        return info

    def save_user(self, info):
        """存储用户信息"""
        info["time"] = self.now()
        self.db["user_info"].update({"_id": info["_id"]}, {"$set": info}, upsert=True)
        return info

    def save_tag_file_num(self, char, num):
        info = {"_id": char, "time": self.now()}
        self.db["search_log"].update({"_id": info["_id"]}, {"$set": info}, upsert=True)

    def save_film_reviews(self, info):
        info["time"] = self.now()
        self.db["film_reviews"].update({"_id": info["_id"]}, {"$set": info}, upsert=True)
        return info

    def find_tag_file_num(self, char):
        res = self.db["search_log"].find_one({"_id": char})
        return res.get("num") if res else 0

    def find_same_tag_film(self, char):
        result = []
        for item in self.db["film_info"].find({"tags": char}):
            result.append(item)
        return result

    def find_file_reviews_by_id(self, id):
        res = self.db["film_reviews"].find_one({"_id": id})
        return self.valid(res)

    def hot_items_ids(self):
        res = self.db["hot_film"].find_one({"_id": str(int(time.time() / 604800))})
        if res:
            return res["hot_film_list"]
        return []

    def save_hot_items(self, film_list):
        res = self.hot_items_ids()
        res = list(set(res + [i[0] for i in film_list]))
        item = {"_id": str(int(time.time() / 604800)), "hot_film_list": res}
        res = self.db["hot_film"].update({"_id": item["_id"]}, {"$set": item}, upsert=True)
        return True


if __name__ == '__main__':
    db = DBUtils()
    # DBUtils().save_file({"_id": "0001", "name": "test1", "tag": ["1", "2", "3"]})
    # print(DBUtils().file_info_by_name("她"))
    c = eval(
        """{'_id': '1307914', 'name': '无间道 無間道 (2002)', 'tags': ['香港', '警匪', '黑帮', '经典', '动作', '犯罪', '剧情', '中国'], 'time': 1524143074}""")
    # print(db.file_info_by_id('1307914'))
    # print([i for i in db.db["film_info"].find()])
    # a = db.find_same_tag_film("黑帮")
    # a = db.save_hot_items([c['_id']])
    # print(a)
    a = db.hot_items_ids()
    # print(len(set(a)))
    print(a)
    pass
