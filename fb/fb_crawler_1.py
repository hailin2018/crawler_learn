# -*- coding: UTF-8 -*-
import requests  # 导入网页请求库
from bs4 import BeautifulSoup  # 导入网页解析库
import pprint
import json
import time
import pandas as pd
import traceback
import numpy as np

# 构造合理的HTTP请求头， 伪装成浏览器， 绕过反爬虫机制
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    'Cookie': 'sb=xpbhXiWldHyUAoo0Z2QxydVV; datr=xpbhXlqRr_p8H-QY9tgjp1Ef; c_user=100052127540124; _fbp=fb.1.1594200476730.1747025338; spin=r.1002530198_b.trunk_t.1597749411_s.1_v.2_; cppo=1; xs=23%3AAb6kKrUl275z0w%3A2%3A1591842752%3A-1%3A-1%3A%3AAcXbb_H_PiXYHmmFE0NQfMnnTKsfWYGrQQhtVXvfi_Q; fr=7WF7YiUhbCiiN8h71.AWUg1cf4nKSoUGpQYJyqQh6trFQ.BesmEA.hm.F81.0.0.BfPIk8.AWVAYzOS; presence=EDvF3EtimeF1597804800EuserFA21B52127540124A2EstateFDutF1597666730781CEchF_7bCC; wd=1871x332',
}

access_token = 'EAACrvkOASWQBANecNrJBNya4Fr18lTQMH99Gp5TNd0LctsRrjQcOXdgmCnUj3pAMCWG37wId5xirLaDnXw5ZBAEZA1UVUh5I9ZAEdoIJiMZBSTuJ1huZCZBYX2WBdeHVo0wKOlP7xc6cq9saddqWeG4kO5h2LfaYQZAFSf1Jhx7PGpa5ThHWwZAKxE2XJ5KeZCD0b2jZBqbPSF4QZDZD'

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


def get_query_id(work_date):

    start_time = int(time.mktime(time.strptime(work_date, "%Y-%m-%d"))) + 54000
    end_time = start_time + 86400

    url = 'https://graph.facebook.com/v5.0/1152079698507696/analytics_cohort_query?access_token={}'.format(access_token)
    queries = '[{"filter_set":"{}","since":start_time,"source":"www/cohorts/universal_builder","until":end_time,"section_load_id":"0a8d8a65-6bce-49be-938c-c4f905a5dc28","breakdown":"$fb.acquisition_source_l1","collation_interval":"DAILY","first_event":{"event_rule":{"application":"1152079698507696","event_name":"fb_mobile_first_app_launch","parameters":[]},"name":"","negate_rule":false},"followup_event":{"event_rule":{"application":"1152079698507696","event_name":"AdImpression","parameters":[]},"name":"","negate_rule":false}}]'
    queries = queries.replace('start_time', str(start_time))
    queries = queries.replace('end_time', str(end_time))

    data = {
        '_index': '50',
        '_reqName': 'object:application/analytics_cohort_query',
        '_reqSrc': 'InsightsGraphAPI',
        'locale': 'zh_CN',
        'method': 'post',
        'pretty': '0',
        'queries': queries,
        'suppress_http_code': '1',
        'xref': 'f1023ffd78484c',  # TODO 随机字符串
    }
    re = requests.post(url, data=data, headers=headers)

    if re.status_code == 200 and 'error' not in re.text:
        qurey_data = re.json()
        query_id = qurey_data['query_ids']
    else:
        query_id = []
    print(query_id, type(query_id))
    return query_id


def get_ananlytics_data(query_id):
    url = 'https://graph.facebook.com/v5.0/1152079698507696/analytics_cohort_query'

    print(type(query_id), type(np.array(query_id)))
    params = {
        'access_token': access_token,
        '_index': '70',
        '_reqName': 'object:application/analytics_cohort_query',
        '_reqSrc': 'InsightsGraphAPI',
        'date_format': 'U',
        'fields': '["query_id","status","data","error"]',
        'locale': 'zh_CN',
        'method': 'get',
        'pretty': '0',
        'query_ids': "{}".format(query_id),
        'suppress_http_code': '1',
        'xref': 'f1655b1da965c1',       # TODO 随机字符串
    }
    re = requests.get(url, params=params, headers=headers)

    print(re.status_code)
    print(re.text)
    ana_result = re.json()['data'][0]
    print(ana_result['query_id'], ana_result['status'])

    ana_data = ana_result['data']['cohorts_data']
    ana_data = json.loads(ana_data)['breakdown_data']
    print(ana_data)

    return ana_data


def main():

    query_id = get_query_id('2020-08-15')
    if not query_id:
        print('未获取到query_id')
        return

    ana_data = get_ananlytics_data(query_id)

    for campaign_id, campaign_data in ana_data.items():
        print(campaign_data)



if __name__ == '__main__':
    result_list = []
    main()
