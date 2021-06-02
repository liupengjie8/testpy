import urllib.request
from bs4 import BeautifulSoup
import pymysql

movieList = []
url = "file:///C:/Users/57567/Desktop/%E9%97%AE%E9%A2%98%E5%BA%93/%E5%88%86%E7%B1%BB.html"


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
    id = 0
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for l1 in l1_list:
        l1_name = l1.find('a', attrs={'class', 'level0'}).get('title')
        id = id + 1
        l1_id = id
        l2_list = l1.findAll('li', attrs={'class', 'level1'})
        print(id)
        save(l1_id,  l1_name, -1,mycursor)
        if l2_list:
            for l2 in l2_list:
                l2_name = l2.find('a', attrs={'class', 'level1'}).get('title')
                id = id + 1
                print(id)
                l2_id = id
                l3_list = l2.findAll('li', attrs={'class', 'level2'})
                save(l2_id, l2_name, l1_id, mycursor)
                if l3_list:
                    for l3 in l3_list:
                        l3_name = l3.find('a', attrs={'class', 'level2'}).get('title')
                        id = id + 1
                        print(id)
                        l3_id = id
                        l41_list = l3.findAll('li', attrs={'class', 'level3'})
                        save(l3_id, l3_name, l2_id, mycursor)
                        if l41_list:
                            for l4 in l41_list:
                                l4_name = l4.find('a', attrs={'class', 'level3'}).get('title')
                                id = id + 1
                                l4_id = id
                                l5_list = l4.findAll('li', attrs={'class', 'level3'})
                                save(l4_id, l4_name, l3_id, mycursor)
                                if l5_list:
                                    for l5 in l5_list:
                                        l5_name = l5.find('a', attrs={'class', 'level4'}).get('title')
                                        id = id + 1
                                        l5_id = id
                                        save(l5_id, l5_name, l4_id ,mycursor)
    conn.commit()
    mycursor.close()
    conn.close()

def save(id,name,parent_id,mycursor):
    print(id,name,parent_id)
    sql = 'INSERT INTO test.blsjf1l (id, name, parent_id) VALUES(%s,%s,%s);'
    mycursor.execute(sql, (id,name,parent_id))

parse_html(get_html(url))

