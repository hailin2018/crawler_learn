# -*- coding: UTF-8 -*-
import requests  # 导入网页请求库
from bs4 import BeautifulSoup  # 导入网页解析库
import pprint
import json
import pandas as pd
import traceback

# 构造合理的HTTP请求头， 伪装成浏览器， 绕过反爬虫机制

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    'Cookie': 'sb=xpbhXiWldHyUAoo0Z2QxydVV; datr=xpbhXlqRr_p8H-QY9tgjp1Ef; c_user=100052127540124; _fbp=fb.1.1594200476730.1747025338; spin=r.1002530198_b.trunk_t.1597749411_s.1_v.2_; cppo=1; xs=23%3AAb6kKrUl275z0w%3A2%3A1591842752%3A-1%3A-1%3A%3AAcXbb_H_PiXYHmmFE0NQfMnnTKsfWYGrQQhtVXvfi_Q; fr=7WF7YiUhbCiiN8h71.AWUg1cf4nKSoUGpQYJyqQh6trFQ.BesmEA.hm.F81.0.0.BfPIk8.AWVAYzOS; presence=EDvF3EtimeF1597804800EuserFA21B52127540124A2EstateFDutF1597666730781CEchF_7bCC; wd=1871x332',
}


# 用于发送请求，获得网页源代码以供解析
# 请求反爬虫网站的源代码会很麻烦，所以单独拿出来
def start_requests(url):
    r = requests.get(url, headers=headers)
    return r


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


def get_query_id(star_time):
    pass

def main():
    url = 'https://www.facebook.com/analytics/1152079698507696/Cohorts/?since=1597104000000&until=1597622400000&__aref_src=entity_selector&__aref_id=entity_selector&force_desktop=true&business_id=2903355609756809&view=DETAILS&cohorts_id=1170127836702882&range_type=LAST_7_DAYS'

    douban_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&page_limit=50&page_start=0'

    dt_url = 'https://graph.facebook.com/v5.0/1152079698507696/analytics_cohort_query?access_token=EAACrvkOASWQBANecNrJBNya4Fr18lTQMH99Gp5TNd0LctsRrjQcOXdgmCnUj3pAMCWG37wId5xirLaDnXw5ZBAEZA1UVUh5I9ZAEdoIJiMZBSTuJ1huZCZBYX2WBdeHVo0wKOlP7xc6cq9saddqWeG4kO5h2LfaYQZAFSf1Jhx7PGpa5ThHWwZAKxE2XJ5KeZCD0b2jZBqbPSF4QZDZD&_index=15&_reqName=object%3Aapplication%2Fanalytics_cohort_query&_reqSrc=InsightsGraphAPI&date_format=U&fields=%5B%22query_id%22%2C%22status%22%2C%22data%22%2C%22error%22%5D&locale=zh_CN&method=get&pretty=0&query_ids=%5B%22ad49d6d726099a0b70310eda9c75b90c%3AV4%22%5D&suppress_http_code=1&xref=f2109cd5a84cbb8'

    re = start_requests(dt_url)
    print(re.text)

    # movie_list = re.json()['subjects']
    # for movie in movie_list:
    #     print(movie)

    # 打印请求头信息
    # print(re.request.headers)
    # print(re.url)


if __name__ == '__main__':
    result_list = []
    main()
