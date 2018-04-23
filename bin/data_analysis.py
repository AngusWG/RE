#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com


class DataAnalysis:
    def __init__(self):
        pass

    @classmethod
    def feature_extraction(cls, tags, file_list):
        res_data = []
        tags = set(tags)
        for item in file_list:
            item["tags"] = same_tag = set(item.get("tags"))
            same_tag = tags & same_tag
            if len(same_tag) > 2:
                item["tags"] = same_tag
                item["len"] = len(same_tag)
                res_data.append(item)
        res_data = sorted(res_data, key=lambda a: a.get("len"), reverse=True)
        return res_data[:int(len(res_data) / 3)]

    @classmethod
    def item_collaboration_filter(cls, user_data):
        """基于物品的协同过滤算法"""
        mylist = user_data
        myset = set(mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
        res = {}
        for item in myset:
            res[item] = mylist.count(item)
        res = sorted(res, key=lambda a: a[1], reverse=True)
        print(res)


if __name__ == '__main__':
    # DataAnalysis.feature_extraction()
    pass
