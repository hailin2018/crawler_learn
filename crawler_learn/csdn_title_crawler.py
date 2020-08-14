# -*- coding: UTF-8 -*-
import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import pprint
import json
import pandas as pd
# 构造合理的HTTP请求头， 伪装成浏览器， 绕过反爬虫机制
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"

douban_url = 'https://movie.douban.com/top250'

csdn_url = 'https://www.csdn.net/'


def get_csdn():
    r = requests.get(csdn_url, headers={'User-Agent': user_agent})
    # print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    get_csdn()
