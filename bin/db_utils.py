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
        return info if self.now() > info["time"] else None

    def file_info_by_name(self, film_name):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"name": film_name})
        return res

    def file_info_by_id(self, id):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"_id": id})
        return res

    def user_info_by_id(self, id):
        """获取一部电影的信息"""
        res = self.db["user_info"].find_one({"_id": id})
        return res

    def file_name_list(self, char=""):
        """搜索数据库中电影的名字集，结果多于X条返回None，名字错误返回False，"""
        result = []
        for item in self.db["name_info"].find({"name": {"$regex": ".*" + char + ".*", "$options": "$i"}}):
            result.append(item["name"])
        return result

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

    def search(self, char):
        result = []
        for item in self.db["film_info"].find({"tags": char}):
            result.append(item)
        return result


if __name__ == '__main__':
    db = DBUtils()
    # DBUtils().save_file({"_id": "0001", "name": "test1", "tag": ["1", "2", "3"]})
    # print(DBUtils().file_info_by_name("她"))
    # print(db.file_info_by_id('1307914'))
    # print([i for i in db.db["film_info"].find()])
    a = db.search("黑帮")

    print(len(set(a)))
    print(a)
    pass
