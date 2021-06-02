import urllib.request
from bs4 import BeautifulSoup
import pymysql

movieList = []
url = "file:///C:/Users/57567/Desktop/test.html"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    ul_zone = soup.find('ul', attrs={'class', 'ztreeLeft'})
    l1_list = ul_zone.findAll('li', attrs={'class', 'level0'})
    handler_list(l1_list)

def handler_list(l1_list):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for l1 in l1_list:
        l1_name = l1.find('a', attrs={'class', 'level0'}).get('title')
        l2_list = l1.findAll('li', attrs={'class', 'level1'})
        if l2_list:
            for l2 in l2_list:
                l2_name = l2.find('a', attrs={'class', 'level1'}).get('title')
                l3_list = l2.findAll('li', attrs={'class', 'level2'})
                if l3_list:
                    for l3 in l3_list:
                        l3_name = l3.find('a', attrs={'class', 'level2'}).get('title')
                        l41_list = l3.findAll('li', attrs={'class', 'level3'})
                        if l41_list:
                            for l4 in l41_list:
                                l4_name = l4.find('a', attrs={'class', 'level3'}).get('title')
                                l5_list = l4.findAll('li', attrs={'class', 'level3'})
                                if l5_list:
                                    for l5 in l5_list:
                                        l5_name = l5.find('a', attrs={'class', 'level4'}).get('title')
                                        save(l1_name, l2_name, l3_name, l4_name, l5_name ,mycursor)
                                else:
                                    save(l1_name, l2_name, l3_name, l4_name, '',mycursor )
                        else:
                            save(l1_name, l2_name, l3_name, '', '', mycursor)
                else:
                    save(l1_name, l2_name, '', '', '', mycursor)
        else:
            save(l1_name,'','','','',mycursor)
    conn.commit()
    mycursor.close()
    conn.close()

def save(l1,l2,l3,l4,l5,mycursor):
    sql = 'INSERT INTO test.blsjfl (level1, level2, level3, level4, level5) VALUES(%s,%s,%s,%s,%s);'
    mycursor.execute(sql, (l1, l2, l3, l4, l5))

parse_html(get_html(url))

