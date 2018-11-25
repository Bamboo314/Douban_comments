# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
@author: Xie Nan
@software: $(PRODUCT_NAME)
@time: 2018/11/25 10:31
"""

import requests
import time
from bs4 import BeautifulSoup
from requests import RequestException
import pandas as pd
import random

# 获取网页源码
def get_html(url):
    try:
        pro = ['222.223.115.30', '112.27.167.74', '221.6.139.154', '114.119.116.93', '183.129.244.17']  # 网上找免费代理
        headers = {
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/subject/26322644/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Cookie': 'yourCookie'
            }

        response = requests.get(url, proxies={'http':random.choice(pro)}, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 使用soup解析html
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


def main():
    # 初始化
    nicknames = []
    dates = []
    evaluates = []
    comments = []
    supports = []

    for pageIndex in range(0, 500, 20):
        # 获取单页的数据
        url = 'https://movie.douban.com/subject/26322644/comments?\
        tart={0}&limit=20&sort=new_score&status=P'.format(
            pageIndex)
        html = get_html(url)
        soup = parse_html(html)
        for nickname in soup.select('#comments a.'):
            nicknames.append(nickname.get_text())
        # print(nicknames)
        # print(len(nicknames))
        for date in soup.select('#comments span.comment-time'):
            dates.append(date.get('title'))
        for evaluate in soup.select('#comments span.rating'):
            evaluates.append(evaluate.get('title'))
        print('start=%i有:' %pageIndex, len(soup.select('#comments span.rating')))  # 因为存在不打分的人
        for comment in soup.select('#comments span.short'):
            comments.append(comment.get_text().replace('\n', ''))
        for support in soup.select('#comments span.votes'):
            supports.append(support.get_text())
        print('爬取第%i页的数据完成' % (pageIndex / 20 + 1))
        time.sleep(1)
    # 查看缺少哪个变量，发现有存在不打分的评论者
    # print(len(nicknames))
    # print(len(dates))
    # print(len(evaluates))
    # print(len(comments))
    # print(len(supports))
    df = pd.DataFrame(list(zip(nicknames, dates, evaluates, comments, supports)),
                      columns=['昵称', '日期', '评价', '短评', '被点赞数'])
    df.to_excel("bailuPlace_short.xlsx")

if __name__  == '__main__':
    main()
