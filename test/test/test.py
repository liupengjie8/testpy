import urllib.request
from bs4 import BeautifulSoup
import pymysql

movieList = []
url = "https://movie.douban.com/top250"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    movie_zone = soup.find('ol', attrs={'class', 'grid_view'})
    movie_list = movie_zone.findAll('li')
    for movie in movie_list:
        movie_name = movie.find('span', attrs={'class', 'title'}).getText()
        movieList.append(movie_name)
        next_page = soup.find('span', attrs={'class', 'next'}).find('a')
    if next_page:
        new_url = url + next_page['href']
        parse_html(get_html(new_url))

def save_movie(movielist):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test')
    mycursor = conn.cursor()
    for id, moviename in enumerate(movielist):
        sql = 'insert into movies values(%s,%s)'
        mycursor.execute(sql, (id, moviename))
    conn.commit()
    mycursor.close()
    conn.close()



parse_html(get_html(url))
save_movie(movieList)

