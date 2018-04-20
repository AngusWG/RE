#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
from urllib.parse import quote

from selenium import webdriver

from bin.log import log


class Crawler:
    def __init__(self, log: log):
        self.max_film = 200
        self.baseURL = "https://movie.douban.com/"
        self.driver = webdriver.PhantomJS(executable_path="./phantomjs.exe")
        self.user_max = 100
        self.log = log
        self.log_count = 0
        self.log.info("爬虫载入成功")

    def __del__(self):
        self.driver.quit()
        self.log.info("爬虫已关闭")
        self.log = None

    def made_log(self):
        self.log.debug(self.driver.current_url)
        self.driver.save_screenshot("test_" + str(self.log_count) + ".png")
        self.log_count = self.log_count + 1

    def film_info_by_name(self, name):
        url = self.baseURL
        self.driver.get(url)
        self.driver.find_element_by_xpath('//*[@id="inp-query"]').send_keys(name)
        self.driver.find_element_by_xpath(
            '//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
        items = self.driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div/div/div[1]/a')
        i = items[0]
        id = i.get_attribute("href")[:-1]
        id = id[id.rfind('/') + 1:]
        return self.film_info_by_id(id)

    def film_info_by_id(self, id):
        id = str(id)
        self.driver.get(self.baseURL + "subject/" + id)
        name = self.driver.find_element_by_xpath('//*[@id="content"]/h1').text
        try:
            tags = self.driver.find_element_by_xpath('//*[@class="tags-body"]').text
            tags = tags.split()
        except TypeError as err:
            self.log.error(id + " " + name + " 没有tags数据", err=err)
            tags = []
        info = {"_id": id, "name": name, "tags": tags}
        self.log.info("{} {} 的信息获取完毕".format(id,name))
        return info

    def film_review_list(self, id):
        """电影评论爬取"""
        id = str(id)
        url = self.baseURL + "subject/" + id + "/comments?sort=time&status=P"
        self.driver.get(url)
        flag = False
        res = []
        while True:
            item = self.driver.find_elements_by_xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/a')
            item = self.driver.find_elements_by_xpath('//span[@class="comment-info"')
            for i in item:
                a = i.get_attribute("href")
                res.append(a.split("/")[-2])
            if len(res) > self.user_max or len(item) < 15:
                print(len(res) , self.user_max , len(item))
                break
            try:
                self.driver.find_element_by_xpath('//*[@id="paginator"]/a').click()
            except:
                self.log.error("下一页按钮 异常")
                break
            self.log.info("已获得 {} 评论数据：{} 条".format(id, len(res) / self.max_film))
        self.log.info("{} 评论数据抓取完成 ".format(id))
        return res

    def user_info(self, id):
        """用户信息爬取"""
        url = self.baseURL + "people/" + id + "/collect"
        self.driver.get(url)
        res = []
        flag = False
        self.log.info("正在抓去用户数据：{} ".format(id))
        while True:
            items = self.driver.find_elements_by_xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[1]/a')
            for i in items:
                id = i.get_attribute("href")[:-1]
                res.append(id[id.rfind('/') + 1:])
            if len(res) > self.max_film or len(items) < 15:
                break
            try:
                self.driver.find_element_by_xpath('//*[@class="next"]').click()
            except:
                self.log.error("下一页按钮 异常")
                break
            self.log.info("已获得{}用户的的数据量：{} ".format(id, len(res) / self.max_film))
        self.log.info("{} 用户数据抓取完成".format(id))
        return res

    def file_name_list(self, name):
        url = self.baseURL
        self.driver.get(url)
        self.driver.find_element_by_xpath('//*[@id="inp-query"]').send_keys(name)
        self.driver.find_element_by_xpath(
            '//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
        items = self.driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div/div/div[1]/a')
        res = []
        for i in items:
            res.append(i.text)
        return res

    def same_tag_list(self, tag):
        page = 0
        url = self.baseURL + "tag/" + quote(tag) + "?start="
        self.driver.get(url + str(page))
        res = []
        self.log.info("开始爬取标签数据 {} ".format(tag))
        while True:
            items = self.driver.find_elements_by_xpath(
                '//div[@class="pl2"]/a')
            for i in items:
                id = i.get_attribute("href")[:-1]
                res.append(id[id.rfind('/') + 1:])
            if len(res) > self.max_film:
                self.log.info("数据量达标", len(res), self.max_film)
                break
            try:
                if not isinstance(self.driver.find_element_by_xpath('//span[@class="next"]/a').text, str):
                    break
                page = page + 20
                self.driver.get(url + str(page))
            except Exception as err:
                self.made_log()
                break
            self.log.info("已获得{}标签的数据量".format(tag), lev3=len(res) / self.max_film)
        self.log.info("{} 标签数据抓取完成 爬取 {} 数据量：{}".format(tag, tag, len(res)))
        return res


if __name__ == '__main__':
    l = log()
    crawler = Crawler(l)
    # crawler.log.error("6636")
    # print(crawler.film_review_list("6722879"))
    # print(crawler.film_info_by_id(1315316))
    # print(crawler.film_info_by_name("她"))
    # print(crawler.user_info("Obtson"))
    # print(crawler.file_name_list("她"))
    # a = crawler.same_tag_list("黑帮")
    #
    # print(len(set(a)))
    # print(a)
    pass
