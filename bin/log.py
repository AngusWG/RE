#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2018/4/17 0017 9:12
# @author  : zza
# @Email   : 740713651@qq.com
import time


class log():
    # __instance = None

    def __init__(self):
        self.errstr = "start " + str(int(time.time())) + "\n"
        self.lev1 = None
        self.lev2 = None
        self.lev3 = None
        self.open = open

    def _del(self):
        with self.open("log.txt", "a", encoding="utf8") as f:
            f.writelines(self.errstr + "\nend")

    def __del__(self):
        with self.open("log.txt", "a", encoding="utf-8") as f:
            str_1 = self.errstr + "\nend " + str(int(time.time())) + "\n\n"
            f.writelines(str_1)

    def debug(self, *args):
        print(*args)

    def info(self, msg, lev1=None, lev2=None, lev3=None, *args):
        if lev3 or self.lev3:
            self.lev3 = lev3 or self.lev3
            msg = str(round(self.lev3, 2) * 100) + "% " + msg
        if lev2 or self.lev2:
            self.lev2 = lev2 or self.lev3
            msg = str(round(self.lev2, 2) * 100) + "% " + msg
        if lev1 or self.lev1:
            self.lev1 = lev1 or self.lev1
            msg = str(round(self.lev1, 2) * 100) + "% " + msg
        print(msg, *args)

    def error(self, msg, url=None, err=None, *args):
        if url:
            print(url)
        print(msg)
        self.errstr += msg + "\n"
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(log, cls).__new__(cls, *args, **kwargs)
    #     return cls.__instance


if __name__ == '__main__':
    # with open("log.txt", "a", encoding="utf8") as f:
    #     f.writelines("sadasd" + "\nend")
    # print("adsad")
    log().errstr = "02123456498"
