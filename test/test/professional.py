import urllib.request
from bs4 import BeautifulSoup
import pymysql
import json

url = "http://rank.cn-healthcare.com/rank/catalogs"


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
        profess_url = "rank/profession-comprehensive-best/" + str(profess["id"]) + "/2018"
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
        if i >= 2:
            profess_rank = i-1
            col_list = hospital.findAll('td')
            hospital_name = col_list[0].findAll('a')[0].getText().strip()
            sybh_value = col_list[1].getText().strip()
            kybh_value = col_list[2].getText().strip()
            comp_value = col_list[3].getText().strip()
            sql = 'insert into professional_rank(professional, professional_rank, sybh_value, kybh_value, comprehensive_value, hospital) values(%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, (profess_name, profess_rank, sybh_value, kybh_value, comp_value, hospital_name))
    conn.commit()
    mycursor.close()
    conn.close()

parse_json(get_html(url))
