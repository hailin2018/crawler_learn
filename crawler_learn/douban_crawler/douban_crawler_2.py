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
基础： 爬取二级页面
"""


# 用于发送请求，获得网页源代码以供解析
# 请求反爬虫网站的源代码会很麻烦，所以单独拿出来
def start_requests(url):
    r = requests.get(url, headers={'User-Agent': user_agent})
    return r.content


# 解析一级网页，获取url列表
def get_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    movies = soup.find_all('div', class_='info')
    pages = []
    for movie in movies:
        url = movie.find('div', class_='hd').a['href']
        pages.append(url)
    return pages


# 解析二级网页，获取信息
def parse_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    mydict = {}
    mydict['title'] = soup.find('span', property='v:itemreviewed').text
    mydict['duration'] = soup.find('span', property='v:runtime').text
    mydict['time'] = soup.find('span', property='v:initialReleaseDate').text
    return mydict


# 将数据读取到json文件中
def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('movies.json', 'w', encoding='utf-8') as f:
        f.write(s)


# 把json文件转化为excel文件
def json_to_excel():
    with open('movies.json', encoding='utf-8') as f:
        s = f.read()
    data = json.loads(s)
    pp = pprint.PrettyPrinter(indent=20)
    # pp.pprint(data)

    df = pd.DataFrame(data)
    # print(df)
    df.to_excel('豆瓣电影.xlsx', sheet_name='豆瓣电影top', index=False)


def main():
    for i in range(7, 9):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        text = start_requests(url)
        pageurls = get_page(text)  # 解析一级页面
        for pageurl in pageurls:  # 解析二级页面
            page = start_requests(pageurl)
            mydict = parse_page(page)
            result_list.append(mydict)
    write_json(result_list)  # 所有电影都存进去之后一起输出到文件
    json_to_excel()


if __name__ == '__main__':
    result_list = []
    main()
