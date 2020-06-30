import urllib.request
from bs4 import BeautifulSoup
import pymysql
import json

url = "http://rank.cn-healthcare.com/rank/catalogs"
year = "2009"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    json_string = request.urlopen(req).read().decode()
    return json_string


def parse_json(json_string):
    json_obj = json.loads(json_string)
    res = json_obj["catalog"]
    profess_list = res
    for profess in profess_list:
        profess_name = profess["cname"]
        profess_url = "rank/profession-reputation-best/" + str(profess["id"]) + "/"+year
        get_profess_rank(profess_name, profess_url)

def get_profess_rank(profess_name, profess_url):
    new_url = "http://rank.cn-healthcare.com/" + profess_url
    soup = BeautifulSoup(get_html(new_url), 'html.parser')
    rank_zone = soup.find('table', attrs={'class', 'table table-bordered text-center'})
    rank_list = rank_zone.findAll('tr')
    save_profess(rank_list, profess_name)


def save_profess(rank_list, profess_name):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for i, hospital in enumerate(rank_list):
        if 11 >= i >= 2:
            profess_rank = i-1
            col_list = hospital.findAll('td')
            if len(col_list) == 5:
                hospital_name = col_list[0].findAll('a')[0].getText().strip()
                province = col_list[1].getText().strip()
                city = col_list[2].getText().strip()
                reputation_value = col_list[3].getText().strip()
                rate = ''
                if col_list[4].findAll('span'):
                    rate = col_list[4].findAll('span')[0].getText().strip()
                    if col_list[4].findAll('span')[1].get('class') == 'arrow-ranking arrow-down col-md-6 col-sm-6 col-xs-6 ' \
                                                                      'text-left':
                        rate = '-' + str(rate)
                    if col_list[4].findAll('span')[1].get('class') == 'arrow-ranking arrow-top col-md-6 col-sm-6 col-xs-6 ' \
                                                                      'text-left':
                        rate = '+' + str(rate)
                sql = 'insert into profession_reputation_best(professional, professional_rank, province, city, reputation_value, rate, hospital, year) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(sql, (profess_name, profess_rank, province, city, reputation_value, rate, hospital_name, year))
    conn.commit()
    mycursor.close()
    conn.close()

parse_json(get_html(url))
