#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
import random
from urllib import parse
from urllib.parse import quote

import selenium
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config
from bin.log import log


class Crawler:
    def __init__(self, film_max, user_max, log: log, filter_degree=0):
        """
        利用phantomjs浏览器与selenium框架实现的爬虫
        :param film_max: 一次爬取中，电影数量的上限
        :param user_max: 一次爬取中，用户数量的上限
        :param log: 日志记录模块
        :param filter_degree: 随机过滤程度 0-9可选，越高随机读取越高
        """
        self.baseURL = "https://movie.douban.com/"
        service_args = ['--ignore-ssl-errors=true',
                        # '--proxy=119.41.168.186:53281', '--proxy-type=https',
                        '--ssl-protocol=TLSv1']
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        # dcap["phantomjs.page.settings.userAgent"] = (random.choice(config.USER_AGENTS))
        dcap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(executable_path="bin/phantomjs.exe", service_args=service_args,
                                          desired_capabilities=dcap)
        self.filter_degree = filter_degree % 10
        self.film_max = film_max
        self.user_max = user_max
        self.log = log
        self.log_count = 0
        self.log.info("爬虫载入成功")

    def __del__(self):
        self.driver.quit()
        self.log.info("爬虫已关闭")
        self.log = None

    def made_log(self):
        """记录错误"""
        self.log.debug(self.driver.current_url)
        self.driver.save_screenshot("test_" + str(self.log_count) + ".png")
        self.log_count = self.log_count + 1

    def film_info_by_id(self, id):
        """通过id获得电影的名称，内容标签"""
        id = str(id)
        self.driver.get(self.baseURL + "subject/" + id)
        self.driver.implicitly_wait(30)
        self.made_log()
        name = self.driver.find_element_by_xpath('//*[@id="content"]/h1').text
        try:
            tags = self.driver.find_element_by_xpath('//*[@class="tags-body"]').text
            tags = tags.split()
        except (TypeError, selenium.common.exceptions.WebDriverException)as err:
            self.made_log()
            self.log.error(id + " " + name + " 没有tags数据", err=err)
            tags = []
        info = {"_id": id, "name": name, "tags": tags}
        self.log.info("{} {} 的信息获取完毕".format(id, name))
        return info

    def judge_fileter(self):
        if random.randint(1, 10) > self.filter_degree:
            return False
        return True

    def film_info_by_name(self, name):
        url = 'https://movie.douban.com/subject_search?search_text={}&cat=1002'.format(parse.quote(name))
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        items = self.driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div/div/div[1]/a')
        i = items[0]
        id = i.get_attribute("href")[:-1]
        id = id[id.rfind('/') + 1:]
        return self.film_info_by_id(id)

    def film_review_list(self, id):
        """电影评论爬取"""
        id = str(id)
        url = self.baseURL + "subject/" + id + "/comments?sort=new_score&status=P&percent_type=h"
        self.driver.get(url)
        res = []
        while True:
            self.driver.implicitly_wait(30)
            item = self.driver.find_elements_by_xpath('//span[@class="comment-info"]')
            if self.judge_fileter():
                continue
            for i in item:
                star = i.find_elements_by_tag_name("span")[1].get_attribute("class")
                if not star == "allstar50 rating":
                    continue
                a = i.find_element_by_tag_name("a").get_attribute("href")
                user_id = str(a.split("/")[-2])
                res.append(user_id)
            if len(res) > self.user_max or len(item) < 15:
                print(len(res), self.user_max, len(item))
                self.made_log()
                break
            try:
                self.driver.find_element_by_xpath('//*[@class="next"]').click()
            except:
                self.log.error("下一页按钮 异常")
                break
            self.log.info("已获得 {} 喜爱用户：{} 个".format(id, len(res)))
        self.log.info(msg="电影编号：{} 喜爱用户抓取完成 ".format(id))
        return res

    def user_info(self, id):
        """用户信息爬取"""
        # todo
        id = str(id)
        num = 0
        url = self.baseURL + "people/" + id + "/collect?start=" + str(num)
        self.driver.get(url)
        res = []
        flag = False
        self.log.info("正在抓去用户数据：{} ".format(id))
        while True:
            self.driver.implicitly_wait(30)
            items = self.driver.find_elements_by_xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[1]/a')
            if self.judge_fileter():
                continue
            for i in items:
                film_id = i.get_attribute("href")[:-1]
                res.append(film_id[film_id.rfind('/') + 1:])
            if len(res) > self.film_max or len(items) < 15:
                break
            try:
                num += 15
                url = self.baseURL + "people/" + id + "/collect?start=" + str(num)
                self.driver.get(url)
            except:
                self.log.error("下一页按钮 异常")
                break
            self.log.info("已获得{}用户的的数据量：{} %".format(id, len(res) * 100 / self.film_max))
        self.log.info("用户id:{} 数据抓取完成".format(id))
        if len(res) == 0:
            self.made_log()
            raise Exception("异常 请检查")
        res = {"_id": id, "films": res}
        return res

    def film_list_by_name(self, name, x=0):
        try:
            url = 'https://movie.douban.com/subject_search?search_text={}&cat=1002'.format(parse.quote(name))
            self.driver.get(url)
            self.driver.implicitly_wait(30)
            items = self.driver.find_elements_by_xpath('//*[@class="title-text"]')
            res = []
            for i in items:
                id = i.get_attribute("href")[:-1]
                res.append({
                    "_id": id[id.rfind('/') + 1:],
                    "name": i.text})
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.WebDriverException)as err:
            self.made_log()
            self.log.error(str(err))
            print(x)
            return self.film_list_by_name(name, x + 1) if x < 20 else []
        return res

    def same_tag_list(self, tag):
        page = 0
        url = self.baseURL + "tag/" + quote(tag) + "?start="
        self.driver.get(url + str(page))
        res = []
        self.log.info("开始爬取标签数据 {} ".format(tag))
        while True:
            self.driver.implicitly_wait(30)
            items = self.driver.find_elements_by_xpath(
                '//div[@class="pl2"]/a')
            if self.judge_fileter():
                continue
            for i in items:
                id = i.get_attribute("href")[:-1]
                res.append(id[id.rfind('/') + 1:])
            if len(res) > self.film_max:
                self.log.info("数据量达标", len(res), self.film_max)
                break
            try:
                if not isinstance(self.driver.find_element_by_xpath('//span[@class="next"]/a').text, str):
                    break
                page = page + 20
                self.driver.get(url + str(page))
            except Exception as err:
                self.made_log()
                break
            self.log.info("已获得{}标签的数据量".format(tag), lev3=len(res) / self.film_max)
        self.log.info("{} 标签数据抓取完成 爬取 {} 数据量：{}".format(tag, tag, len(res)))
        return res


if __name__ == '__main__':
    pass
