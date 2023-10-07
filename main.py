#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import os

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Cookie": "SUB=_2AkMThUH3f8NxqwJRmPAQzGPhZI11zAzEieKl2bAsJRMxHRl-yT9yqlU9tRB6OAVvGCUJgPCUyXmOV8nAYUSl3rbOKkcW; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WheGXqZH3GKo6PYLnXWbNhr; _s_tentry=passport.weibo.com; Apache=482074338451.52136.1691995842045; SINAGLOBAL=482074338451.52136.1691995842045; ULV=1691995842069:1:1:1:482074338451.52136.1691995842045:"
}

weibo_url = "https://s.weibo.com/top/summary/"
zhihu_url = "https://www.zhihu.com/billboard?utm_id=0"
news_list = []


def generate_news():
    print("begin parser zhihu")
    parser_zhihu()
    print("begin parser weibo")
    parser_weibo()
    print("begin write md")
    write_md()


def parser_weibo():
    news_list.append("## 微博\n")
    res = requests.get(weibo_url, timeout=10, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    lis = soup.select('section li')
    for li in lis:
        href = 'https://s.weibo.com' + li.select('a')[0]['href']
        # 移除强调标签
        for tag in li.findAll('em'):
            tag.extract()
        title = li.select('span')[0].get_text()
        news_list.append(f'- [{title}]({href})<br/>\n')
    news_list.append("---\n")


def parser_zhihu():
    news_list.append("## 知乎\n")
    res = requests.get(zhihu_url, timeout=10, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('#js-initialData')[0].get_text()
    hot_list = json.loads(data)['initialState']['topstory']['hotList']
    for topic in hot_list:
        title = topic['target']['titleArea']['text']
        href = topic['target']['link']['url']
        news_list.append(f'- [{title}]({href})<br/>\n')
    news_list.append("---\n")


def write_md():
    today_ = str(datetime.date.today())
    month_ = today_[0:7]
    cur_dir = os.path.join(os.getcwd(), '_posts')
    if not os.path.exists(cur_dir):
        os.mkdir(cur_dir)
    file_name = today_ + '-NEWS.md'
    with open(os.path.join(cur_dir, file_name), 'w', encoding='utf-8') as load_f:
        load_f.write('---\n')
        load_f.write('layout: post\n')
        load_f.write(f'title: "{today_}-news"\n')
        load_f.write(f'date: {today_} 08:00:00 -0000\n')
        load_f.write(f'categories: {month_}\n')
        load_f.write('---\n')
        load_f.write('\n')

        for line in news_list:
            load_f.writelines(line + '\n')

    with open(os.path.join(os.getcwd(), "index.md"), 'w', encoding='utf-8') as load_me:
        load_me.write(f'<h1 align="center">👋 {today_} 每日新闻</h1>\n')
        load_me.write('\n')
        load_me.writelines(news_list)


if __name__ == '__main__':
    generate_news()
