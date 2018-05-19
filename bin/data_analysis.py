#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com


class DataAnalysis:

    @classmethod
    def feature_extraction(cls, tags, file_list):
        """基于标签的过滤"""
        res_data = []
        tags = set(tags)
        print("共{}部电影".format(len(file_list)))
        for item in file_list:
            item["tags"] = same_tag = set(item.get("tags"))
            same_tag = tags & same_tag
            if len(same_tag) > 2:
                item["tags"] = same_tag
                item["len"] = len(same_tag)
                res_data.append(item)
        res_data = sorted(res_data, key=lambda a: a.get("len"), reverse=True)
        return res_data

    @classmethod
    def item_collaboration_filter(cls, user_data):
        """基于物品的协同过滤算法"""
        mylist = user_data
        myset = set(mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复项
        res = {}
        for item in myset:
            res[item] = mylist.count(item)
        res = sorted(res.items(), key=lambda a: a[1], reverse=True)
        print("共{}部电影".format(len(res)))
        res_data = list()
        # 去掉少数项目
        for k, v in res:
            if v == 1:
                continue
            res_data.append((k, v))
        return res_data

    @staticmethod
    def calc_same_tag(*arg):
        """计算电影数据的相同内容标签"""
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
        return data


if __name__ == '__main__':
    # DataAnalysis.feature_extraction()
    pass
