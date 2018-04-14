#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
from bin.db_utils import DBUtils
from bin.scrapy import Scrapy


class Server:
    """接受来自界面的各种请求"""

    def __init__(self):
        self.scrapy = Scrapy()
        self.db = DBUtils()

    def film_name_list(self):
        """快速检查用"""
        pass

    def same_attributes(self):
        """基于相同属性的推荐电影"""
        pass

    def same_taste(self):
        """基于相同品味的推荐电影"""
        pass
