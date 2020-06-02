import urllib.request
from bs4 import BeautifulSoup
import pymysql
import json
from jsonpath import jsonpath

movieList = []
url = "http://rank.cn-healthcare.com/rank/catalogs"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    print(file)
    soup = BeautifulSoup(file, 'html.parser')
    profess_zone = soup.find('div', attrs={'id', 'slected-search-sort'})
    print(profess_zone)
    profess_list = profess_zone.findAll('p')
    for profess in profess_list:
        profess_name = profess.find('a').getText()
        profess_url = profess.find('a')['href']
        get_profess_rank(profess_name, profess_url)

def get_profess_rank(profess_name, profess_url):
    new_url = "http://rank.cn-healthcare.com/" + profess_url
    soup = BeautifulSoup(get_html(new_url), 'html.parser')
    rank_zone = soup.find('div', attrs={'class', 'table table-bordered text-center'})
    rank_list = rank_zone.findAll('tr')
    save_movie(rank_list, profess_name)


def save_movie(rank_list, profess_name):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for i, hospital in enumerate(rank_list):
        profess_rank = i+1
        hos_id = hospital['hosid']
        region = hospital['region']
        hosname = hospital['hosname']
        category = hospital['category']
        col_list = hospital.findAll('td')
        hospital = col_list[0]
        sybh_value = col_list[1]
        kybh_value = col_list[2]
        comprehensive_value = col_list[3]
        sql = 'insert into professional_rank values(%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(sql, (profess_rank, profess_name, profess_rank, sybh_value, kybh_value, comprehensive_value, hospital))
    conn.commit()
    mycursor.close()
    conn.close()

parse_html(get_html(url))
