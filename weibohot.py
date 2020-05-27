#!/usr/bin/env python
#coding:utf-8

import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import weibohotDAO as dao
import configparser
import os
import schedule
import time


# 定义变量
# url_weibohot = 'https://s.weibo.com/top/summary?cate=realtimehot' 
# response = requests.get(url_weibohot)
# if response:
#     #print(response.text)
#     bs = BeautifulSoup(response.text, 'html.parser')
#     realtimehot = bs.find(id="pl_top_realtimehot")
#     tbody = realtimehot.find("tbody")
#     lines = tbody.find_all("tr")
#     tops = []
#     for line in lines:
#         topn = {}
#         if line.find('td',class_="td-01 ranktop") is not None:
#             topn["rank"] = line.find('td',class_="td-01 ranktop").string
#             topn["topic"] = line.find('td',class_="td-02").a.get_text()
#             topn["hot"] = line.find('td',class_="td-02").span.get_text()
#             topn["hottype"] = line.find('td',class_="td-03").string if line.find('td',class_="td-03").string is not None else ''
#             tops.append(dict(topn))
#             topn.clear()
#     # print(tops)
#     conn = dao.get_conn('weibohot.db', 'sqlite')
#     for t in tops:
#         dao.hot_insert(conn, t)
#     dao.dao_commit(conn)
#     dao.dao_close(conn)
# else:
#     print("请求失败！")

class weibohot():

    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.configPath = os.path.join(self.root_path, "config.txt")
        self.conf = configparser.ConfigParser()
        self.conf.read("config.txt")
        self.url = self.conf.get("url", "url_weibohot")  # 获取指定section 的option值
        self.dbtype = self.conf.get("db", "dbtype")
        self.dbname = self.conf.get("db", "dbname")


    def get_weibohot(self):
        response = requests.get(self.url)
        if response:
            bs = BeautifulSoup(response.text, 'html.parser')
            realtimehot = bs.find(id="pl_top_realtimehot")
            tbody = realtimehot.find("tbody")
            lines = tbody.find_all("tr")
            tops = []
            for line in lines:
                topn = {}
                if line.find('td',class_="td-01 ranktop") is not None:
                    topn["rank"] = line.find('td',class_="td-01 ranktop").string
                    topn["topic"] = line.find('td',class_="td-02").a.get_text()
                    topn["hot"] = line.find('td',class_="td-02").span.get_text()
                    topn["hottype"] = line.find('td',class_="td-03").string if line.find('td',class_="td-03").string is not None else ''
                    tops.append(dict(topn))
                    topn.clear()
            # print(tops)
            conn = dao.get_conn('weibohot.db', 'sqlite')
            for t in tops:
                dao.hot_insert(conn, t)
            dao.dao_commit(conn)
            dao.dao_close(conn)
        else:
            print("请求失败！")

if __name__ == "__main__":
    weibohot = weibohot()
    schedule.every(1).minutes.do(weibohot.get_weibohot)
    while True:
        schedule.run_pending() # 运行所有可运行的任务
        time.sleep(1)