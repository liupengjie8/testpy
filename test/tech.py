import urllib.request
import json
import pymysql
from bs4 import BeautifulSoup
import requests

movieList = []
url = "http://top100.imicams.ac.cn/subject"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    dept_zone = soup.find('ul', attrs={'class', 'nav_left'})
    dept_list = dept_zone.findAll('li')
    for dept in dept_list:
        dept_name = dept.find('a').getText()
        dept_code = dept.find('a')['id'][9:]
        for year in range(2013, 2019):
            ajaxHandler(dept_code, year, dept_name)

def ajaxHandler(subject, year, dept_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
               'Accept': 'application/json, text/javascript, */*; q=0.01', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest'}
    s = requests.Session()
    urls = 'http://top100.imicams.ac.cn/public/ranking/rankingAction_searchRankByCode.action'
    data = {'subject': subject, 'year': year, 'start': 1, 'end': 100}
    content = s.post(urls, data=data, headers=headers)
    json_obj = json.loads(content.content)
    save_rank_list(json_obj["rows"], year, dept_name)

def save_rank_list(rank_list, year, dept_name):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for column in rank_list:
        if year == '2017' or year == '2018':
            sql = 'insert into test.tech_value (YEAR, SUBJECT, sort, hospital, tech_output, academic_influence, tech_condition, VALUE) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, (year, dept_name, column["RANK"], column["HOSPNAME"], column["INPUT"], column["OUTPUT"], column["INFLUENCE"], column["SUM"]))
        else:
            sql = 'insert into test.tech_value (YEAR, SUBJECT, sort, hospital, tech_output, academic_influence, tech_condition, VALUE) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, (year, dept_name, column["RANK"], column["HOSPNAME"], column["OUTPUT"], column["INFLUENCE"], column["INPUT"],column["SUM"]))
    conn.commit()
    mycursor.close()
    conn.close()



parse_html(get_html(url))




