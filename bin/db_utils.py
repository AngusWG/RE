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

    def file_info_by_name(self, film_name):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"name": film_name})
        return res

    def file_info_by_id(self, id):
        """获取一部电影的信息"""
        res = self.db["film_info"].find_one({"_id": id})
        # if res.count() == 0:
        #     return None
        return res

    def file_name_list(self, char=""):
        """搜索数据库中电影的名字集，结果多于X条返回None，名字错误返回False，"""
        result = []
        for item in self.db["name_info"].find({"name": {"$regex": ".*" + char + ".*", "$options": "$i"}}):
            result.append(item["name"])
        return result

    def db_check(self):
        try:
            re = pymongo.MongoClient("www.4yewu.cn", 27017)["RE"]
            re["log"].insert_one(
                {"_id": time.time(), "name": socket.gethostname(), "ip": socket.gethostbyname(socket.gethostname())})
        except pymongo.errors.ServerSelectionTimeoutError as err:
            log().error("无法连接到数据，请通知管理员", err)
            return None
        return re

    def save_info(self, info):
        """"""
        self.db["film_info"].update({"_id": info["_id"]}, {"$set": info}, upsert=True)
        return info


if __name__ == '__main__':
    # DBUtils().save_info({"_id": "0001", "name": "test1", "tag": ["1", "2", "3"]})
    print(DBUtils().file_info_by_name("她"))
