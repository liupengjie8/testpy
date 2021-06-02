import urllib.request
from bs4 import BeautifulSoup
import pymysql
import json


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    return request.urlopen(req).read().decode()


def get_rank(html, year):
    soup = BeautifulSoup(html, 'html.parser')
    rank_zone = soup.find('table', attrs={'class', 'table table-bordered text-center'})
    rank_list = rank_zone.findAll('tr')
    save_rank_list(rank_list, year)


def save_rank_list(rank_list, year):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for i, hospital in enumerate(rank_list):
        if i >= 2:
            rank = i - 1
            col_list = hospital.findAll('td')
            hospital_name = col_list[0].findAll('a')[0].getText().strip()
            sybh_value = col_list[1].getText().strip()
            kybh_value = col_list[2].getText().strip()
            comp_value = col_list[3].getText().strip()
            rate = ''
            if col_list[4].findAll('span'):
                rate = col_list[4].findAll('span')[0].getText().strip()
                if col_list[4].findAll('span')[1].get('class') == 'arrow-ranking arrow-down col-md-6 col-sm-6 col-xs-6 ' \
                                                                  'text-left':
                    rate = '-' + str(rate)
                if col_list[4].findAll('span')[1].get('class') == 'arrow-ranking arrow-top col-md-6 col-sm-6 col-xs-6 ' \
                                                                  'text-left':
                    rate = '+' + str(rate)
            sql = 'insert into general_best(rank, sybh_value, kybh_value, comprehensive_value, hospital, rate, year) values(%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, (rank, sybh_value, kybh_value, comp_value, hospital_name, rate, year))
    conn.commit()
    mycursor.close()
    conn.close()


def handler_url():
    for i in range(2009, 2019):
        url = "http://rank.cn-healthcare.com/rank/general-best/" + str(i)
        get_rank(get_html(url), i)


handler_url()
