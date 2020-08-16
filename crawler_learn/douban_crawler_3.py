# -*- coding: UTF-8 -*-
import requests  # 导入网页请求库
from bs4 import BeautifulSoup  # 导入网页解析库
import pprint
import json
import pandas as pd
import traceback

# 构造合理的HTTP请求头， 伪装成浏览器， 绕过反爬虫机制
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"

"""
基础： 爬取二级页面，并改用类的形式
"""


class Doubantop(object):

    def __init__(self):
        self.baseurl = 'https://movie.douban.com/top250?start={}&filter='
        self.result_list = []

    def start_requests(self, url):
        r = requests.get(url, headers={'User-Agent': user_agent})
        return r.content

    def get_page(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        movies = soup.find_all('div', class_='info')
        pages = []
        for movie in movies:
            url = movie.find('div', class_='hd').a['href']
            pages.append(url)
        return pages

    def parse_page(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        movies = soup.find_all('div', class_='info')
        pages = []
        for movie in movies:
            url = movie.find('div', class_='hd').a['href']
            pages.append(url)
        return pages

    def start_requests(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        mydict = {}
        mydict['title'] = soup.find('span', property='v:itemreviewed').text
        mydict['duration'] = soup.find('span', property='v:runtime').text
        mydict['time'] = soup.find('span', property='v:initialReleaseDate').text
        return mydict

    def write_json(self, result_list):
        s = json.dumps(result_list, indent=4, ensure_ascii=False)
        with open('movies.json', 'w', encoding='utf-8') as f:
            f.write(s)

    # 把json文件转化为excel文件
    def json_to_excel(self):
        with open('movies.json', encoding='utf-8') as f:
            s = f.read()
        data = json.loads(s)
        pp = pprint.PrettyPrinter(indent=20)
        # pp.pprint(data)

        df = pd.DataFrame(data)
        # print(df)
        df.to_excel('豆瓣电影.xlsx', sheet_name='豆瓣电影top', index=False)

    def start(self):
        for i in range(7, 9):
            url = self.baseurl.format(i * 25)
            text = self.start_requests(url)
            pageurls = self.get_page(text)  # 解析一级页面
            for pageurl in pageurls:  # 解析二级页面
                page = self.start_requests(pageurl)
                mydict = self.parse_page(page)
                self.result_list.append(mydict)
        self.write_json(self.result_list)  # 所有电影都存进去之后一起输出到文件
        self.json_to_excel()


if __name__ == '__main__':

    douban = Doubantop()
    douban.start()
