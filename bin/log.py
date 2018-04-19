#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2018/4/17 0017 9:12
# @author  : zza
# @Email   : 740713651@qq.com

class log():
    __instance = None

    def debug(self, *args):
        print(*args)

    def info(self, *args):
        print(*args)

    def error(self, msg, err=None, url=None, *args):
        if url:
            print(url)
        print(msg)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(log, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
