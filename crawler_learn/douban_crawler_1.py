# -*- coding: UTF-8 -*-
import requests  # 导入网页请求库
from bs4 import BeautifulSoup  # 导入网页解析库
import pprint
import json
import pandas as pd
import traceback

# 构造合理的HTTP请求头， 伪装成浏览器， 绕过反爬虫机制
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"

douban_url = 'https://movie.douban.com/top250'

csdn_url = 'https://www.csdn.net/'

"""
基础：爬去简单页面，多个网页的url可以手动构造
"""


# 用于发送请求，获得网页源代码以供解析
# 请求反爬虫网站的源代码会很麻烦，所以单独拿出来
def start_requests(url):
    r = requests.get(url, headers={'User-Agent': user_agent})
    return r.content


# 接收网页源代码解析出需要的信息
def parse(text):
    soup = BeautifulSoup(text, 'html.parser')
    movie_list = soup.find_all('div', attrs={'class': "item"})

    for movie_info in movie_list:
        try:
            info = {}
            title = movie_info.find('span', class_='title').text
            score = movie_info.find('span', class_='rating_num').text
            quote = movie_info.find('span', class_='inq').text
            bd = movie_info.find('div', class_='bd')
            number_text = bd.find_all('span')[-2].text[:-3]
            info['title'] = title
            info['score'] = score
            info['quote'] = quote
            info['number'] = number_text
            result_list.append(info)
        except Exception as e:
            print('\n')
            traceback.print_exc()
            print(movie_info)
            continue


# 将数据写入json文件
def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('movies_250.json', 'w', encoding='utf-8') as f:
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
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        text = start_requests(url)
        parse(text)
        print('第 {} 页抓取完毕'.format(i+1))
    write_json(result_list)


if __name__ == '__main__':
    result_list = []

    main()
